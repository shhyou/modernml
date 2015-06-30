import json

FILE_LIST = ["apress", "oreilly-data-id.json", "mit.json"]
ITEM_VOCABS_FILE = "item-vocabs.json"
VOCABS_IDF_FILE = "vocabs-idf.json"

GRAM_MAX = 4

DOCUMENT_LIST = {}

for fil in FILE_LIST:
  with open(fil, "r") as filp:
    data = json.load(filp)
  for item in data:
    DOCUMENT_LIST[item[u"id"]] = item

with open(ITEM_VOCABS_FILE, "r") as filp:
  ITEM_VOCABS_ = [{u"id": vocab[u"id"], u"vocabs": set(vocab[u"vocabs"]) } \
                  for vocab in json.load(filp)]

ITEM_VOCABS = {}
for vocab in ITEM_VOCABS_:
  ITEM_VOCABS[vocab[u"id"]] = vocab

with open(VOCABS_IDF_FILE, "r") as filp:
  VOCABS_IDF = json.load(filp)

