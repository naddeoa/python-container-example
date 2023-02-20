from whylogs.core.resolvers import MetricSpec, ResolverSpec
from whylogs.core.schema import DeclarativeSchema, DatasetSchema
from typing import Dict
from whylabs_toolkit.container.config_types import DatasetCadence, DatasetOptions, DatasetUploadCadence, DatasetUploadCadenceGranularity
from whylogs.experimental.extras.embedding_metric import (
    DistanceFunction,
    EmbeddingConfig,
    EmbeddingMetric,
)
from whylogs.experimental.preprocess.embeddings.selectors import PCAKMeansSelector
import os.path as path

# Parse the embeddings file
embeddings = []
dir = path.dirname(path.abspath(__file__))
with open(f'{dir}/glove.6B.100d.txt', 'r') as f:
    for line in f.readlines():
        split = line.split(' ')
        split.pop(0)
        embedding = [float(it) for it in split]
        embeddings.append(embedding)

# Embeddings configuration
references, _ = PCAKMeansSelector(n_clusters=8, n_components=20).calculate_references(embeddings)
config = EmbeddingConfig(
    references=references,
    labels=None,
    distance_fn=DistanceFunction.euclidean,
)

schema = DeclarativeSchema([ResolverSpec(column_name="embeddings", metrics=[MetricSpec(EmbeddingMetric, config)])])


# Export a dictionary of dataset id to DatasetSchemas for the container to use
schemas: Dict[str, DatasetOptions] = {
    'model-17': DatasetOptions(
        schema=schema,
        dataset_cadence=DatasetCadence.HOURLY,
        whylabs_upload_cadence=DatasetUploadCadence(
            granularity=DatasetUploadCadenceGranularity.MINUTE,
            interval=5
        )
    )
}