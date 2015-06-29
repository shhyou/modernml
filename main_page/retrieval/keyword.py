import common

def generate(ids, limit=2147483647):
  """Generate terminologies related to ids

  ids: A list of integers. The IDs of related items.
  returns: A list of strings, each of which is a terminology.
  """

  counts = [{} for i in xrange(common.GRAM_MAX)]
  for vocab in [vocab for item in ids for vocab in common.ITEM_VOCABS[item][u"vocabs"]]:
    gram = vocab.count(" ")
    if vocab not in counts[gram]:
      counts[gram][vocab] = 1
    else:
      counts[gram][vocab] += 1

  vs = []
  for i in xrange(common.GRAM_MAX-1,-1,-1):
    vocabcounts = [(counts[i][v]*(i+1)*(i+1), i+1, v) for v in counts[i]]
    vocabcounts.sort()
    vocabcounts.reverse()
    vocabcounts = vocabcounts[:limit]
    vs += vocabcounts
    if i > 0:
      for c, _, v in vocabcounts:
        vw = v.split()
        v1 = " ".join(vw[1:])
        v2 = " ".join(vw[:-1])
        counts[i-1][v1] -= c
        counts[i-1][v2] -= c
  vs.sort()
  vs.reverse()
  return [v for _, _, v in vs][:limit]

if __name__ == "__main__":
  print "keyword test"
