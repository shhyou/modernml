import common
import stemstop
from item_search import search

import math
import json
import pprint

pp = pprint.PrettyPrinter(indent=2)

THRESHOLD = 0.8
GROUP_SIZE = 5

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
    return (vector, position, w_list, set(vector.keys()), book_id)

def cos(n1, n2):
    return sum(n1[0][w]*n2[0][w] for w in n1[3] & n2[3])

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
        node_list = []
        for _id in ids:
            len_toc = len(common.DOCUMENT_LIST[_id]['toc'])
            for i,topic in enumerate(common.DOCUMENT_LIST[_id]['toc']):
                tmp = stemstop.simpl_stopwords_split(topic.lower())
                tmp = stemstop.stems(tmp)
                node_list.append(create_node(tmp, float(i)/len_toc, _id))

        self.p = [i for i in xrange(len(node_list))]

        for i in xrange(len(node_list)):
            for j in xrange(i+1,len(node_list)):
                if cos(node_list[i],node_list[j]) > THRESHOLD:
                    if self.find_p(i) != self.find_p(j):
                        self.p[self.p[i]] = self.p[j]

        for i in xrange(len(node_list)):
            pa = self.find_p(i)
            if pa in self.group:
                self.group[pa].append(node_list[i])
            else:
                self.group[pa] = [node_list[i]]

        res = [(sum(n[1] for n in self.group[g])/len(self.group[g]),self.group[g]) for g in self.group if len(self.group[g]) > GROUP_SIZE]
        res.sort()

        res_json = {"toc":[]}
        for r in res:
            toc = {"topic":" ".join(r[1][0][2]), "item":[]}
            for n in r[1]:
                item = {}
                item["title"] = common.DOCUMENT_LIST[n[4]]["title"]
                item["href"] = common.DOCUMENT_LIST[n[4]]["href"]
                item["topic"] = " ".join(n[2])
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
