#!/usr/bin/env python2

import json

res = []
for fil in ["apress", "oreilly-data-id.json", "mit.json"]:
  with open(fil, "r") as filp:
    data = json.load(filp)
  for item in data:
    words = [w for sec in item[u"toc"] for w in sec.split()]
    words = [w.replace("'s", "").replace(",", "") for w in words]
    words = [w.lower() for w in words]
    words = [w for w in words if w != u"&"]
    # TODO: stemming and stopwords
    words = words \
          + [" ".join(ws) for ws in zip(words, words[1:])] \
          + [" ".join(ws) for ws in zip(words, words[1:], words[2:])]
    words = list(set(words))
    words.sort()
    res.append({u"id": item[u"id"], u"vocabs": words})

with open("item-vocabs.json", "w") as filp:
  json.dump(res, filp)
