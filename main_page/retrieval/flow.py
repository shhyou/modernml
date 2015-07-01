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
                node = create_node(tmp, float(i)/len_toc, _id)
                for w in tmp:
                    if w in node_bucket:
                        node_bucket[w].append((all_node_num, node))
                    else:
                        node_bucket[w] = [(all_node_num, node)]
                all_node_list.append(node)
                all_node_num += 1

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

        res = [(sum(n["rank"] for n in self.group[g])/len(self.group[g]),self.group[g]) for g in self.group if len(self.group[g]) > GROUP_SIZE]
        res.sort()

        res_json = {"toc":[]}
        for r in res:
            toc = {"topic":" ".join(r[1][0]["vocabs"]), "item":[]}
            for n in r[1]:
                item = {}
                item["title"] = common.DOCUMENT_LIST[n["id"]]["title"]
                item["href"] = common.DOCUMENT_LIST[n["id"]]["href"]
                item["topic"] = " ".join(n["vocabs"])
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
