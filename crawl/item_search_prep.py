#!/usr/bin/env python2

import json
import stoplist

GRAM_MAX = 4
PUNCTUATIONS = stoplist.PUNCTUATIONS.split()
STOP_WORDS = set(stoplist.STOP_WORDS.split())

def simpl_stopwords_split(s):
  for punc in PUNCTUATIONS:
    s = s.replace(punc, "")
  return [w for w in s.split() if not (w in STOP_WORDS or w.isdigit())]

def accum_ngrams(n, words): # compute i-gram for i in xrange(n)
  return [" ".join(ws) for i in xrange(n) \
                       for ws in zip(*(words[j:] for j in xrange(i+1)))]

res = []
for fil in ["apress", "oreilly-data-id.json", "mit.json"]:
  with open(fil, "r") as filp:
    data = json.load(filp)
  for item in data:
    # TODO: stemming and stopwords
    words = [w for sec in item[u"toc"] for w in accum_ngrams(GRAM_MAX, simpl_stopwords_split(sec.lower()))]
    words = list(set(words))
    words.sort()
    res.append({u"id": item[u"id"], u"vocabs": words})

with open("item-vocabs.json", "w") as filp:
  json.dump(res, filp)
