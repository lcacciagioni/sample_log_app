import falcon
import os
import socket
import json


class EnvResources:
    def on_get(self, req, resp):
        """
        This get will show yo the env vars that will be logged to the stdout
        and stderr
        """
        resp.status = falcon.HTTP_200
        msg = """Hey I'm running at: %s:%s\n
And this is the VCAP_APPLICATION json: \n%s""" \
            % (self.get_host(), self.get_port(), self.get_vcap_env())
        resp.body = msg
        print(msg)

    def get_host(self):
        """
        This function will exract the warden container ip from the socket info
        WARNING: This is not a healthy way to do this as you can see this needs
        a host to stablish a connection resulting in a very high cost for
        performance PLASE DO NOT DO THIS IN PROD!!!
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("api.cfv2.dspdev.wmg.com", 80))
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
        return json.dumps(json.loads(os.environ['VCAP_APPLICATION']),
                          sort_keys=True, indent=4)


app = falcon.API()
envs = EnvResources()
app.add_route('/', envs)
