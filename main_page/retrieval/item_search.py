import configs

import json

def search(keywords):
  """Search related books/courses from the keywords

  keywords: A list of string. Search keywords;
  returns: A list of integers representing IDs of related items
  """

  # Possibly TODO: normalize keywords (stopwords & stemming & cases)
  ids = []
  for fil in configs.FILE_LIST:
    with open(fil, "r") as filp:
      data = json.load(filp)
    for item in data:
      if any([section for section in item[u"toc"] if keyword in section] \
             for keyword in keywords):
        ids.append(item[u"id"])
  ids.sort()
  return list(set(ids))

if __name__ == "__main__":
  print "search_book test?"
  print "Python\n", search([u"Python"])
  print "python\n", search([u"python"])
  print "\nmachine learning"
  print search([u"machine learning"])
  print search([u"machine", u"learning"])
