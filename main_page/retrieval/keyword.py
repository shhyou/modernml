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
  vs = list(v for v, c in vocab_count.items() if c > 10)
  vs.sort()
  vs.reverse()
  return vs

if __name__ == "__main__":
  print "keyword test"
