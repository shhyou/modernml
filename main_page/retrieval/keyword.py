import configs

def generate(ids):
  """Generate terminologies related to ids

  ids: A list of integers. The IDs of related items.
  returns: A list of strings, each of which is a terminology.
  """

  vocab_count = {}
  for item in ids:
    for vocab in configs.ITEM_VOCABS[item][u"vocabs"]:
      if vocab not in vocab_count:
        vocab_count[vocab] = 1
      else:
        vocab_count[vocab] = vocab_count[vocab] + 1
  vs = list((c, v.count(" "), v) for v, c in vocab_count.items() if " " in v)
  vs.sort()
  vs.reverse()
  zs = []
  counts = dict((v, c) for c, _, v in vs)
  for c, gram, v in vs:
    if gram == 3:
      zs.append((c, gram, v))
      ws = v.split()
      w1, w2 = ws[0]+" "+ws[1], ws[1]+" "+ws[2]
      if w1 in counts:
        counts[w1] = counts[w1] - c
      if w2 in counts:
        counts[w2] = counts[w2] - c
    elif gram == 2:
      c_ = counts.pop(v)
      zs.append((c_, gram, v))

  zs.sort()
  zs.reverse()
  return [v for _, _, v in zs]

if __name__ == "__main__":
  print "keyword test"
