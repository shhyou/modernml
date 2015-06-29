#!/usr/bin/env python2

import json

for fil in ["apress", "oreilly-data-id.json"]:
  with open(fil, "r") as filp:
    data = json.load(filp)
  res = []
  for item in data:
    words = [w for sec in item[u"toc"] for w in sec.split()]
    words = [w.replace("'s", "") for w in words]
    words = [w.lower() for w in words]
    words = [w for w in words if w != u"&"]
    words = list(set(words))
    words.sort()
    res.append({u"id": item[u"id"], u"vocabs": words})

with open("item-vocabs.json", "w") as filp:
  json.dump(res, filp)
