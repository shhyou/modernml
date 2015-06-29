#!/usr/bin/env python2

import json
import stoplist

PUNCTUATIONS = stoplist.PUNCTUATIONS.split()
STOP_WORDS = set(stoplist.STOP_WORDS.split())

def simpl_stopwords_split(s):
  for punc in PUNCTUATIONS:
    s = s.replace(punc, "")
  return [w for w in s.split() if not (w in STOP_WORDS or w.isdigit())]

res = []
for fil in ["apress", "oreilly-data-id.json", "mit.json"]:
  with open(fil, "r") as filp:
    data = json.load(filp)
  for item in data:
    words = [w for sec in item[u"toc"] for w in simpl_stopwords_split(sec.lower())]
    # TODO: stemming and stopwords
    words = words \
          + [" ".join(ws) for ws in zip(words, words[1:])] \
          + [" ".join(ws) for ws in zip(words, words[1:], words[2:])] \
          + [" ".join(ws) for ws in zip(words, words[1:], words[2:], words[3:])]
    words = list(set(words))
    words.sort()
    res.append({u"id": item[u"id"], u"vocabs": words})

with open("item-vocabs.json", "w") as filp:
  json.dump(res, filp)
