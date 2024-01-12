from collections import defaultdict
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

from thirdai import bolt, data

from .documents import DocumentDataSource
from .models import CancelState, Mach, Model
from .sharded_documents import shard_data_source
from .supervised_datasource import SupDataSource
from .utils import clean_text, requires_condition

InferSamples = List
Predictions = Sequence
TrainLabels = List
TrainSamples = List


class MachMixture(Model):
    def __init__(
        self,
        number_models: int,
        id_col: str = "DOC_ID",
        id_delimiter: str = " ",
        query_col: str = "QUERY",
        fhr: int = 50_000,
        embedding_dimension: int = 2048,
        extreme_output_dim: int = 10_000,  # for Mach Mixture, we use default dim of 10k
        extreme_num_hashes: int = 8,
        model_config=None,
        label_to_segment_map: defaultdict = None,
        seed_for_sharding: int = 0,
    ):
        self.id_col = id_col
        self.id_delimiter = id_delimiter
        self.query_col = query_col
        self.fhr = fhr
        self.embedding_dimension = embedding_dimension
        self.extreme_output_dim = extreme_output_dim
        self.extreme_num_hashes = extreme_num_hashes
        self.n_ids = 0
        self.model_config = model_config

        # These parameters are specific to Mach Mixture
        self.number_models = number_models

        if label_to_segment_map == None:
            self.label_to_segment_map = defaultdict(list)
        else:
            self.label_to_segment_map = label_to_segment_map

        self.seed_for_sharding = seed_for_sharding

        self.models: List[Mach] = [
            Mach(
                id_col=self.id_col,
                id_delimiter=self.id_delimiter,
                query_col=self.query_col,
                fhr=self.fhr,
                embedding_dimension=self.embedding_dimension,
                extreme_output_dim=self.extreme_output_dim,
                extreme_num_hashes=self.extreme_num_hashes,
                model_config=self.model_config,
            )
            for _ in range(self.number_models)
        ]

    def set_mach_sampling_threshold(self, threshold: float):
        if self.models is None:
            raise Exception(
                "Cannot set Sampling Threshold for a model that has not been"
                " initialized"
            )

        for model in self.models:
            model.set_mach_sampling_threshold(threshold)

    def get_model(self) -> List[bolt.UniversalDeepTransformer]:
        return self.models

    def set_model(self, models):
        self.models = models

    def save_meta(self, directory: Path):
        if self.models is not None:
            for model in self.models:
                model.save_meta(directory)

    def load_meta(self, directory: Path):
        if self.models is not None:
            for model in self.models:
                model.load_meta(directory)

    def set_n_ids(self, n_ids: int):
        self.n_ids = n_ids

    def get_query_col(self) -> str:
        return self.query_col

    def get_id_col(self) -> str:
        return self.id_col

    def get_id_delimiter(self) -> str:
        return self.id_delimiter

    def index_documents(
        self,
        intro_documents: DocumentDataSource,
        train_documents: DocumentDataSource,
        should_train: bool,
        fast_approximation: bool = True,
        num_buckets_to_sample: Optional[int] = None,
        on_progress: Callable = lambda **kwargs: None,
        cancel_state: CancelState = None,
        max_in_memory_batches: int = None,
        variable_length: Optional[
            data.transformations.VariableLengthConfig
        ] = data.transformations.VariableLengthConfig(),
        **kwargs,
    ) -> None:
        # We need the original number of classes from the original data source so that we can initialize the Mach models this mixture will have
        number_classes = intro_documents.size

        # Make a sharded data source with introduce documents. When we call shard_data_source, this will shard the introduce data source, return a list of data sources, and modify the label index to keep track of what label goes to what shard
        introduce_data_sources = shard_data_source(
            data_source=intro_documents,
            label_to_segment_map=self.label_to_segment_map,
            number_shards=self.number_models,
            update_segment_map=True,
        )

        # Once the introduce datasource has been sharded, we can use the update label index to shard the training data source ( We do not want training samples to go to a Mach model that does not contain their labels)
        train_data_sources = shard_data_source(
            train_documents,
            label_to_segment_map=self.label_to_segment_map,
            number_shards=self.number_models,
            update_segment_map=False,
        )

        self.n_ids += intro_documents.size

        for intro_shard, train_shard, model in zip(
            introduce_data_sources, train_data_sources, self.models
        ):
            model.index_documents(
                intro_documents=intro_shard,
                train_documents=train_shard,
                should_train=should_train,
                fast_approximation=fast_approximation,
                num_buckets_to_sample=num_buckets_to_sample,
                on_progress=on_progress,
                cancel_state=cancel_state,
                max_in_memory_batches=max_in_memory_batches,
                override_number_classes=number_classes,
                variable_length=variable_length,
                **kwargs,
            )

    def delete_entities(self, entities) -> None:
        for model in self.models:
            model.delete_entities(entities)

    def forget_documents(self) -> None:
        for model in self.models:
            model.forget_documents()
        self.n_ids = 0

    @property
    def searchable(self) -> bool:
        return self.n_ids != 0

    def infer_labels(
        self, samples: InferSamples, n_results: int, **kwargs
    ) -> Predictions:
        for model in self.models:
            model.model.set_decode_params(
                min(self.n_ids, n_results), min(self.n_ids, 100)
            )

        per_model_results = bolt.UniversalDeepTransformer.parallel_inference(
            models=[model.model for model in self.models],
            batch=[{self.query_col: clean_text(text)} for text in samples],
        )

        results = []
        for index in range(len(samples)):
            sample_results = []
            for y in per_model_results:
                sample_results.extend(y[index])
            sample_results.sort(key=lambda x: x[1], reverse=True)
            results.append(sample_results[:n_results])
        return results

    @requires_condition(
        check_func=lambda x: False,
        method_name="score",
        method_class="MachMixture",
        condition_unmet_string="when multiple models are initialized",
    )
    def score(
        self, samples: InferSamples, entities: List[List[int]], n_results: int = None
    ) -> Predictions:
        pass

    @requires_condition(
        check_func=lambda x: False,
        method_name="score",
        method_class="MachMixture",
        condition_unmet_string="when multiple models are initialized",
    )
    def infer_buckets(
        self, samples: InferSamples, n_results: int, **kwargs
    ) -> Predictions:
        pass

    def associate(
        self,
        pairs: List[Tuple[str, str]],
        n_buckets: int,
        n_association_samples: int = 16,
        n_balancing_samples: int = 50,
        learning_rate: float = 0.001,
        epochs: int = 3,
    ):
        for model in self.models:
            model.associate(
                pairs=pairs,
                n_buckets=n_buckets,
                n_association_samples=n_association_samples,
                n_balancing_samples=n_balancing_samples,
                learning_rate=learning_rate,
                epochs=epochs,
            )

    def _shard_upvote_pairs(
        self, source_target_pairs: List[Tuple[str, int]]
    ) -> List[List[Tuple[str, int]]]:
        shards = [[] for _ in range(self.number_models)]
        for pair in source_target_pairs:
            model_ids = self.label_to_segment_map.get(pair[1])
            if model_ids is None:
                raise Exception(f"The Label {pair[1]} is not a part of Label Index")
            for model_id in model_ids:
                shards[model_id].append(pair)
        return shards

    def upvote(
        self,
        pairs: List[Tuple[str, int]],
        n_upvote_samples: int = 16,
        n_balancing_samples: int = 50,
        learning_rate: float = 0.001,
        epochs: int = 3,
    ):
        sharded_pairs = self._shard_upvote_pairs(pairs)

        for model, shard in zip(self.models, sharded_pairs):
            if len(shard) == 0:
                continue
            model.upvote(
                pairs=shard,
                n_upvote_samples=n_upvote_samples,
                n_balancing_samples=n_balancing_samples,
                learning_rate=learning_rate,
                epochs=epochs,
            )

    def retrain(
        self,
        balancing_data: DocumentDataSource,
        source_target_pairs: List[Tuple[str, str]],
        n_buckets: int,
        learning_rate: float,
        epochs: int,
    ):
        balancing_data_shards = shard_data_source(
            data_source=balancing_data,
            number_shards=self.number_models,
            label_to_segment_map=self.label_to_segment_map,
            update_segment_map=False,
        )
        for model, shard in zip(self.models, balancing_data_shards):
            model.retrain(
                balancing_data=shard,
                source_target_pairs=source_target_pairs,
                n_buckets=n_buckets,
                learning_rate=learning_rate,
                epochs=epochs,
            )

    def __setstate__(self, state):
        if "model_config" not in state:
            # Add model_config field if an older model is being loaded.
            state["model_config"] = None
        self.__dict__.update(state)

    def train_on_supervised_data_source(
        self,
        supervised_data_source: SupDataSource,
        learning_rate: float,
        epochs: int,
        batch_size: Optional[int],
        max_in_memory_batches: Optional[int],
        metrics: List[str],
        callbacks: List[bolt.train.callbacks.Callback],
    ):
        supervised_data_source_shards = shard_data_source(
            data_source=supervised_data_source,
            number_shards=self.number_models,
            label_to_segment_map=self.label_to_segment_map,
            update_segment_map=False,
        )

        for shard, model in zip(supervised_data_source_shards, self.models):
            if shard.size == 0:
                continue
            model.train_on_supervised_data_source(
                supervised_data_source=shard,
                learning_rate=learning_rate,
                epochs=epochs,
                batch_size=batch_size,
                max_in_memory_batches=max_in_memory_batches,
                metrics=metrics,
                callbacks=callbacks,
            )
