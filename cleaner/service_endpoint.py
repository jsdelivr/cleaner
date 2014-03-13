#http://support.deployhq.com/kb/advanced-settings/setting-up-notifications
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from blinker import signal
import json
import logging

class EndPoint(Protocol):

    pub_key = None

    def __init__(self):
        try:
            with open("public_key.pub") as f:
                self.pub_key = f.read().replace('\n', '')
                f.close()
        except Exception, e:
            pass

    def dataReceived(self, jsondata):
        logging.debug("Recieved data... " + jsondata)
        data = json.loads(jsondata)

        if self.pub_key and self.pub_key != data["files"]["project"]["public_key"]:
            #respond 403
            return
        if data["status"] != "completed":
            return

        signal("redeploy").send(data)

def start(port=4040):
    logging.info("Attempting to open our end point on port: %d", (port))
    fact = Factory()
    fact.protocol = EndPoint
    reactor.listenTCP(port, fact)
    reactor.run()
    logging.info("Now listening to port %d", (port))