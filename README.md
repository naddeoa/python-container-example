
Sample project that demonstrates how to the whylogs container with custom
whylogs configuration to enable features like embeddings.

This only applies to the new python based whylogs container. The original java
based whylogs container can't be extended like this.


## What you need

- A folder named `whylogs_config`
- A file named `whylogs_config/config.py`
- A variable in `whylogs_config/config.py` named `schemas` of type `Dict[str, DatasetOptions]`
- Optional: Anything that should be deployed along with the container should go
    into `whylogs_config/config.py`
- A Dockerfile that copies your `whylogs_config` folder into the right spot (see
    the Dockerfile in this repo)


At startup, the container is going to try `from ...whylogs_config.config import schemas`. If there is something there then it will be used to configure the whylogs loggers in the container. The `schemas` var is a map from dataset id to configuration options. The container will be tied to a single org and api key.

