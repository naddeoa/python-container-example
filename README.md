
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
docker build . -t my-whylogs-container
docker run -it --net=host --env-file local.env my-whylogs-container
```

## Configuring

There are two types of config. Simple config that can be passed via env variables and custom config that is specified as python source and built into the container.

### Env configuration
Here are the current env configuration options. These should be stored in a `.env` file and passed to docker when running the container.

```
##
## REQUIRED CONFIG
##

# Your WhyLabs org id
WHYLABS_ORG_ID=org-0
# An api key from the org above
WHYLABS_API_KEY=xxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

##
## OPTIONAL CONFIG
##

# Safeguard if you're using custom configuration to guarantee the container is correctly built to use it.
FAIL_STARTUP_WITHOUT_CONFIG=True

# If you don't care about password protecting the container then you can set this to True.
DISABLE_CONTAINER_PASSWORD=True

# Sets the container password to `password`. See the auth section for details
CONTAINER_PASSWORD=password

# The default dataset type to use between HOURLY and DAILY. This determines how data is grouped up into
# profiles before being uploaded. You need to make sure this matches what you configured the dataset as
# in your WhyLabs settings page.
DEFAULT_WHYLABS_DATASET_CADENCE=HOURLY | DAILY

# The frequency that uploads occur, being denoted in either minutes (M), hours (H), or days (D).
DEFAULT_WHYLABS_UPLOAD_CADENCE=M | H | D
# The interval, given the configured cadence. Setting this to 15 with a cadence of M would result in uploads every 15 minutes.
DEFAULT_WHYLABS_UPLOAD_INTERVAL=15
```

### Custom configuration

This repo shows the project structure you need if you want to use custom configuration. You would need to use this type of configuration if your use case requires you to use a schema with whylogs. Some examples of use cases would be embeddings and segments. This repo demonstrates an embedding configuration in `whylogs_config/config.py`. The file path is important. Anything along side that file path will also be bundled with the container if you use the Dockerfile here, which is useful if you need to use embeddings. You can also use custom configuration to independently configure multiple datasets, rather than having them all fallback to the defaults set in the env variables.

The python dependencies in this package don't actually matter. They're just installed os that you can use an IDE to create the configuration file. You can use any of the dependencies that are already packaged in the [base container](https://github.com/whylabs/whylogs-container-python/blob/master/pyproject.toml#L10), things like pandas, nympy, whylogs, etc.

## Auth

If the container is configured to use a password then you'll have to send a special auth header along with requests. If the password is set to `my-password` then the header (in curl format) would be

```
-H "Authorization: Bearer my-password"
```

## Calling

### Directly via HTTP
There isn't a published client yet (coming soon), so requests can be made via http calls using the `requests` module. See examples folder for a calling example. There are examples for logging normal tabular data as well as embeddings, which require custom configuration.

### Google Pub\Sub
The container has a special endpoint that takes requests forwarded from Google pub\sub: `/log-pubsub` and `/log-pubsub-embeddings`. You'll send the same payloads that you would send to the container directly, except you'll send them to pub\sub and they'll be forwarded instead. Don't do any extra escaping on your json data. 