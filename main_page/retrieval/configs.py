import json

FILE_LIST = ["apress", "oreilly-data-id.json", "mit.json"]
ITEM_VOCABS_FILE = "item-vocabs.json"

with open(ITEM_VOCABS_FILE, "r") as filp:
  ITEM_VOCABS_ = [{u"id": vocab[u"id"], u"vocabs": set(vocab[u"vocabs"]) } \
                  for vocab in json.load(filp)]

ITEM_VOCABS = {}
for vocab in ITEM_VOCABS_:
  ITEM_VOCABS[vocab[u"id"]] = vocab

import stoplist
PUNCTUATIONS = stoplist.PUNCTUATIONS.split()
STOP_WORDS = set(stoplist.STOP_WORDS.split())
