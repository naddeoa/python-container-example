from whylogs.core.resolvers import MetricSpec, ResolverSpec
import os
import time
import pandas as pd
import numpy as np
from whylogs.core.schema import DeclarativeSchema
from whylogs.core import DatasetProfile
from typing import Dict
from whylabs_toolkit.container.config_types import DatasetCadence, DatasetOptions, DatasetUploadCadence, DatasetUploadCadenceGranularity
from whylogs.experimental.extras.embedding_metric import (
    DistanceFunction,
    EmbeddingConfig,
    EmbeddingMetric,
)
from whylogs.experimental.preprocess.embeddings.selectors import PCAKMeansSelector
import os.path as path
from typing import List

# Parse the embeddings file
embeddings: List[List[float]] = []
dir = path.dirname(path.abspath(__file__))
with open(f'{dir}/glove.6B.50d.txt', 'r') as f:
    for line in f.readlines():
        split = line.split(' ')
        split.pop(0)
        embedding = [float(it) for it in split]
        embeddings.append(embedding)

# Embeddings configuration
references, _ = PCAKMeansSelector(n_clusters=8, n_components=20).calculate_references(np.asarray(embeddings))
config = EmbeddingConfig(
    references=references,
    labels=None,
    distance_fn=DistanceFunction.euclidean,
)

schema = DeclarativeSchema([ResolverSpec(column_name="embeddings", metrics=[MetricSpec(EmbeddingMetric, config)])])
profile1 = DatasetProfile(schema=schema)

df = pd.read_csv(f'{dir}/lending_club.csv')

## BROKEN PROFILE
print('')
print('=================================')
print('starting profiling with schema')
print('=================================')
print('')
start = time.perf_counter()
profile1.track(df)
print(profile1.view().to_pandas())
print(f'finished after {time.perf_counter() - start}')
profile1.view().write('./profile.bin')

## WORKING PROFILE
print('')
print('=================================')
print('starting profiling without schema (it works)')
print('=================================')
print('')
profile2 = DatasetProfile()
start = time.perf_counter()
profile2.track(df)
print(profile2.view().to_pandas())
print(f'finished after {time.perf_counter() - start}')
profile2.view().write('./profile.bin')

