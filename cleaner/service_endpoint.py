#http://support.deployhq.com/kb/advanced-settings/setting-up-notifications
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from blinker import signal
import json
import logging

from Crypto.PublicKey import RSA

class EndPoint(Protocol):

    pub_key = None
    public_key_file = "public_key.pub"

    def __init__(self):
        try:
            with open(self.public_key_file) as f:
                self.pub_key = RSA.importKey(f.read())
                f.close()
        except Exception, e:
            logging.warn("No public key given in %s -- Triggers will not be verified", public_key_file)

    def dataReceived(self, jsondata):
        logging.debug("Recieved data... " + jsondata)
        data = json.loads(jsondata)

        
        if data["status"] != "completed":
            return
        # validate request signature
        given_key = RSA.importKey(data["files"]["project"]["public_key"])
        if self.pub_key and self.pub_key != given_key:
            #respond 403
            return

        signal("redeploy").send(data)

def start(port=4040):
    logging.info("Attempting to open our end point on port: %d", (port))
    fact = Factory()
    fact.protocol = EndPoint

    reactor.listenTCP(port, fact)
    logging.info("Now listening to port %d", (port))
    reactor.run()