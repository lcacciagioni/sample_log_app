import falcon
import os
import socket
import json
import logging
from logstash_formatter import LogstashFormatter

logger = logging.getLogger('cf-env')
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(
    'syslogserver.example.com', 514))
formatter = LogstashFormatter()

handler.setFormatter(formatter)
logger.addHandler(handler)


class EnvResources:
    def on_get(self, req, resp):
        """
        This get will show yo the env vars that will be logged to the stdout
        and stderr
        """
        resp.status = falcon.HTTP_200
        msg = """Hey  I'm running at: %s:%s""" \
            % (self.get_host(), self.get_port())
        resp.body = msg
        env_vars = self.get_vcap_env()
        logger.info("Test message",
                    extra={"instance_index":
                           env_vars['instance_index'],
                           "port": env_vars['port'],
                           "mem_limit": env_vars['limits']['mem']})

    def get_host(self):
        """
        This function will exract the warden container ip from the socket info
        WARNING: This is not a healthy way to do this as you can see this needs
        a host to stablish a connection resulting in a very high cost for
        performance PLASE DO NOT DO THIS IN PROD!!!
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        return(s.getsockname()[0])

    def get_port(self):
        """
        This function will get the port where your app is listening
        """
        try:
            return os.environ['PORT']
        except:
            return None

    def get_vcap_env(self):
        """
        This will return a dict from the json object that we can find in the
        ENV var VCAP_APPLICATION
        """
        return json.loads(os.environ['VCAP_APPLICATION'])


app = falcon.API()
envs = EnvResources()

# Here as you can see you will be able to edit from where this log is comming
# for more information see:
# https://github.com/exoscale/python-logstash-formatter#usage

formatter.source_host = "cf-env-%s" % (
    envs.get_vcap_env()['instance_index'])

app.add_route('/', envs)
