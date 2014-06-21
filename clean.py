from os import environ as environment
import argparse, yaml
import logging
from cleaner import Cleaner

parser = argparse.ArgumentParser()
parser.add_argument("--path", help="path to run cleaner on", type=str)
args = parser.parse_args()

# logging.basicConfig(level=logging.DEBUG)


with open("config.yml") as sets:
    config = yaml.load(sets)

path = args.path
if not path:
	path = config["cleaner"]["general_pattern"]

cleaner = Cleaner(config["cleaner"])

print "Cleaning path: " + str(path)
cleaner.clean(path, True)