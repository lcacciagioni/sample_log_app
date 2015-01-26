# sample_log_app
Sample app to log from CF to the outside world

## Running this app
```
$ cf push cf-env -b https://github.com/cloudfoundry/python-buildpack.git -c "gunicorn -c example_config.py app:app"
```
