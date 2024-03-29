import common
import stemstop
from item_search import search

import math
import json
import pprint

pp = pprint.PrettyPrinter(indent=2)

THRESHOLD = 0.5
GROUP_SIZE = 4
GRAM = 2

BUZZ_WORDS = [u"introduction", u"homework", u"wrap", u"exercis", u"exercise", \
              u"real", u"multi", u"summary", u"context", u"application", \
              u"overview", u"reference", u"conclusion", u"problem", \
              u"exploration", u"colophon", u"paper", u"project", \
              u"homework problem", u"resource", u"short", u"short paper", \
              u"keynote" , u"talk" , u"keynote talk", u"preface", u"simple", \
              u"simple application", u"building", u"invited", u"invited talk", \
              u"background", u"assumption", u"basic", u"foundation", \
              u"fundamental", u"contribution", u"contributed", \
              u"contributed paper", u"book", u"transform", u"concept", \
              u"notation", u"basic concept", u"definition", u"properties", \
              u"started", u"fine", u"scope", u"statement", u"high", \
              u"invited paper", u"test", u"bibliography", u"computer", \
              u"final", u"exam", u"final exam", u"putting", u"midterm", \
              u"midterm exam", u"appendix", u"reading", u"chapter", \
              u"chapter summary", u"quiz", u"solution", u"solution chapter", \
              u"extra", u"extra topic", u"topic review", u"review", \
              u"selected", u"selected solution", u"selected reference", \
              u"note", u"wrapping", u"thing", u"wrapping thing", \
              u"figure", u"learned"]

def accum_ngrams(n, words): # compute i-gram for i in xrange(n)
  return [" ".join(ws) for i in xrange(0,n) \
                       for ws in zip(*(words[j:] for j in xrange(i+1)))]

def create_node(w_list, position, book_id):
    #v_len = math.sqrt(len(w_list))
    vector = {}
    for w in w_list:
        if w in vector:
            vector[w] += common.VOCABS_IDF[w]
        else:
            vector[w]  = common.VOCABS_IDF[w]
    v_len = math.sqrt(sum(vector[w]**2 for w in vector))
    for w in vector:
        vector[w] /= v_len
    return dict(vector=vector, keys=set(vector.keys()), rank=position, \
                vocabs=w_list, id=book_id)

def cos(n1, n2):
    return sum(n1["vector"][w]*n2["vector"][w] for w in n1["keys"] & n2["keys"])

class flow_agent():
    def __init__(self):
        self.p = []
        self.group = {}

    def find_p(self,i):
        if self.p[i] == i:
            return i
        else:
            self.p[i] = self.find_p(self.p[i])
            return self.p[i]

    def generate(self, ids):
        node_bucket = {}
        all_node_num = 0
        all_node_list = []
        for _id in ids:
            len_toc = len(common.DOCUMENT_LIST[_id]['toc'])
            for i,topic in enumerate(common.DOCUMENT_LIST[_id]['toc']):
                tmp = stemstop.simpl_stopwords_split(topic.lower())
                tmp = stemstop.stems(tmp)
                tmp = accum_ngrams(GRAM, tmp)
                node = create_node(tmp, float(i)/len_toc, _id)
                for w in tmp:
                    if w in node_bucket:
                        node_bucket[w].append((all_node_num, node))
                    else:
                        node_bucket[w] = [(all_node_num, node)]
                all_node_list.append(node)
                all_node_num += 1

        for buzz_word in BUZZ_WORDS:
            if buzz_word in node_bucket:
                node_bucket.pop(buzz_word)

        self.p = [i for i in xrange(all_node_num)]

        for node_list in node_bucket.itervalues():
            node_num = len(node_list)
            for i in xrange(node_num):
                for j in xrange(i+1,node_num):
                    idx1, nod1 = node_list[i]
                    idx2, nod2 = node_list[j]
                    if cos(nod1, nod2) > THRESHOLD:
                        if self.find_p(idx1) != self.find_p(idx2):
                            self.p[self.p[idx1]] = self.p[idx2]

        for i in xrange(all_node_num):
            pa = self.find_p(i)
            if pa in self.group:
                self.group[pa].append(all_node_list[i])
            else:
                self.group[pa] = [all_node_list[i]]

        res = [( sum(n["rank"] for n in self.group[g])/len(self.group[g])/len(set(node["id"] for node in self.group[g])), \
                self.group[g]) \
               for g in self.group if len(self.group[g]) > GROUP_SIZE]
        res.sort()

        res_json = {"toc":[]}
        for r in res:
            toc = {"topic":"; ".join(r[1][0]["vocabs"]), "item":[]}
            for n in r[1]:
                item = {}
                item["title"] = common.DOCUMENT_LIST[n["id"]]["title"]
                item["href"] = common.DOCUMENT_LIST[n["id"]]["href"]
                item["topic"] = ", ".join(n["vocabs"])
                toc["item"].append(item)
            res_json["toc"].append(toc)
        return json.dumps(res_json) 

def generate(ids):
    """Generate

    ids: A list of integers. The IDs of related items.
    returns: Learning flow. See $TOP/main_page/README.md
    """
    fa = flow_agent()
    return fa.generate(ids)

if __name__ == '__main__':
    pp.pprint(json.loads(generate(search(u'machine learning'))))
