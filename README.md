# sample_log_app
Sample app to log from an app deployed in Cloud Foundry to any syslog server. This app try's to capture and show the real ip & port where your app is running.

> Getting the real IP & PORT (DEA IP & PORT) where your app is running is almost impossible before CF v196 so **be careful**.-

## Requirements
You will need a running syslog server that could be reached by the app. Any of the following can be used:

* [rsyslog](http://www.rsyslog.com/receiving-messages-from-a-remote-system/)
* [Logstash](http://logstash.net/docs/1.4.2/tutorials/getting-started-with-logstash)
* [Graylog](https://www.digitalocean.com/community/tutorials/how-to-install-graylog2-and-centralize-logs-on-ubuntu-14-04)

Cloud Foundry: **>=v196** This is because we use the env vars CF_INSTANCE which has been introduced in this version. You can check [here](https://github.com/cloudfoundry/cf-release/releases/tag/v196) & [here](https://www.pivotaltracker.com/n/projects/966314/stories/82311924). This means that if you use an older version of CF this app will not work.

## Running this app

```
$ cf push
$ cf se cf-env SYSLOG_URL syslog.example.com
$ cf se cf-env SYSLOG_PORT 5000
$ cf restage cf-env
```

This command will use the default configs stored in the `manifest.yml` file to deploy this app in Cloud Foundry.
Then with the second and the third command you will set the configuration variables matching to your syslog server deployment and the last command will ensure that your app will capture and use the changes that you have made.

## Recomendations for Logstash

Syslog is great but it has some limits on the message size that could make the application debugging really hard!!! So if you want a superior option I can recommend to use the [GELF input](http://logstash.net/docs/1.4.2/inputs/gelf) or [collectd input](http://logstash.net/docs/1.4.2/inputs/collectd). Here are some links:

* [log4j GELF Adapter](https://github.com/Graylog2/log4j2-gelf)
* [graypy](https://pypi.python.org/pypi/graypy)
* [ruby GELF Adapter](https://github.com/Graylog2/gelf-rb)
* [Custom Ruby Logger](https://github.com/dwbutler/logstash-logger)
* [Tomcat Sample Config](http://blog.lanyonm.org/articles/2014/01/12/logstash-multiline-tomcat-log-parsing.html) - Tomcat is the default server used in Java deployments in CF
* [Logstash Load Balancing 1](http://blog.lusis.org/blog/2012/01/31/load-balancing-logstash-with-redis/)
* [Logstash Load Balancing 2](http://logstash.net/docs/1.4.2/tutorials/just-enough-rabbitmq-for-logstash)
* [Grok Filtering Tutorial 1](https://home.regit.org/2014/01/a-bit-of-logstash-cooking/)
* [Kibana Dashborads Tutorial](http://www.elasticsearch.org/guide/en/kibana/current/using-kibana-for-the-first-time.html)

> The [default](http://docs.cloudfoundry.org/devguide/services/log-management.html) cf approach for apps use syslog streaming which has the limits already mentioned.-
