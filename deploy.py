from blinker import signal
import os

from cleaner import Clean_Repo, create_server

import logging

logging.basicConfig(level=logging.DEBUG)

# start her up and create subs
cleaner = Clean_Repo()

def handler(data):
	cleaner.clean(data.files.changed)

signal("redeploy").connect(handler)

#clean the entire server at script start
cleaner.cleanAll()

# 4040 is the first num to pop into my head
port = int(os.environ.get("PORT", 4040))
create_server(port)