from blinker import signal
from os import environ as environment
import yaml, logging, argparse

from cleaner import Clean_Repo, create_server

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("--debug", help="debug statements + verbose",
                    action="store_true")
args = parser.parse_args()

level = logging.WARNING
if args.debug:
    level = logging.DEBUG
elif args.verbose:
    level = logging.INFO
logging.basicConfig(level=level) #filename="logging.log", filemode="a", datefmt='%m-%d %H:%M',


with open("config.yml") as sets:
    config = yaml.load(sets)

# start her up and create subs
cleaner = Clean_Repo(config["cleaner"])

def handler(data):
    cleaner.clean(data["files"]["changed"])

signal("redeploy").connect(handler)

#clean the entire server at script start
cleaner.cleanAll()

port = int(environment.get("PORT", config["port"]))
# create_server(port)