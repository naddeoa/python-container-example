
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


## Running

### No Custom Config
If you want to run the container without any custom configuration then you don't
have to worry about the Dockerfile or python code. You can just run the
following

```bash
docker run -it --net=host --env-file local.env whylabs/whylogs:py-latest
```

With a `local.env` file with your whylabs credentials.

```
WHYLABS_ORG_ID=org-xxxx
WHYLABS_API_KEY=xxxx
```

### With Custom Config

After you create your python config (like this repo demonstrates) and you create
a Dockerfile similar to the one in this repo you'll be able to build the image
and run the container.

```
docker build . -t my-whylogs-contianer
docker run -it --net=host --env-file local.env my-whylogs-contianer
```

