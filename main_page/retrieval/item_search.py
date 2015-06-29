import configs

import json

with open(configs.ITEM_VOCABS, "r") as filp:
  item_vocabs = [{u"id": vocab[u"id"], u"vocabs": set(vocab[u"vocabs"]) } \
                 for vocab in json.load(filp)]

def search(keywords):
  """Search related books/courses from the keywords

  keywords: A list of string. Search keywords; the keywords are used as 'conjuction'
  returns: A list of integers representing IDs of related items
  """

  # Possibly TODO: normalize keywords (stopwords & stemming & cases)
  keywords = [keyword.lower().replace("'s", "") for keyword in keywords]

  itsets = []
  for i, keyword in enumerate(keywords):
    itsets.append([])
    for vocab in item_vocabs:
      if keyword in vocab["vocabs"]:
        itsets[i].append(vocab[u"id"])
    itsets[i] = set(itsets[i])

  ids = itsets[0]
  for idlist in itsets:
    ids &= idlist
  return list(ids)

if __name__ == "__main__":
  print "item_search test"
  print "python\n", search([u"python"])
  print "\nmachine learning"
  print search([u"machine", u"learning"])
