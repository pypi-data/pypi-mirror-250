# wrapper
A python implementation wrapping and serving the user semantic lambdas 

## setup

### python

1. requires python3.10
* brew install python@3.10

2. requires a venv
* venv create:
* ```python3 -m venv ~/.venv/wrapper --upgrade-deps```
* venv activate:
* ```source ~/.venv/wrapper/bin/activate```
* venv deactivate: ```deactivate```

3. install requirements
* pip install -r requirements.txt

### Local development
To develop a local pydirect server, complete the following steps:

Start the proxy server from the root directory
```commandline
# Point python path to local wrapper before launching server
$ export LOCAL_APP_PATH=<wrapper path> && export PYTHONPATH=$PYTHONPATH:$LOCAL_APP_PATH
$ python -m wrapper.main --toml_path=$LOCAL_APP_PATH/pyproject.toml
```

Validate server is functioning and healthy
```commandline
$ curl http://127.0.0.1:8000/healthcheck
> {"status":"ok"}                    
```

### Fly.io deployment
To deploy a pydirect server to fly.io, complete the following steps:

#### Install flyctl
```commandline
brew install flyctl
```

#### Login to fly.io
In your browser, navigate to fly.io and login using shared credentials in 1password


#### Auth flyctl
```commandline
flyctl auth login
```

#### Deploy
```commandline
flyctl deploy
```
