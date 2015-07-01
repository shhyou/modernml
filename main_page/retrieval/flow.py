import common
import stemstop
import math
import json
from item_search import search

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

def cos(n1, n2 ):
    return sum(n1[0][w]*n2[0][w] for w in n1[3] & n2[3])

class flow_agent():
    def __init__(self):
        self.node_list = []
        self.p = []
        self.node_list = []
        self.group = {}

    def find_p(self,i):
        if self.p[i] == i:
            return i
        else:
            self.p[i] = self.find_p(self.p[i])
            return self.p[i]

    def generate(self, ids):
        for _id in ids:
            len_toc = len(common.DOCUMENT_LIST[_id]['toc'])
            for i,topic in enumerate(common.DOCUMENT_LIST[_id]['toc']):
                tmp = stemstop.simpl_stopwords_split(topic.lower())
                tmp = stemstop.stems(tmp)
                #print tmp
                self.node_list.append(create_node(tmp, float(i)/len_toc, _id))
        #print len(node_list)
        for i in xrange(len(self.node_list)):
            self.p.append(i)
        num = 0
        for i in xrange(len(self.node_list)):
            #if visit[i]: continue
            for j in xrange(i+1,len(self.node_list)):
                #if find_p(i) == find_p(j): continue
                num += 1
                if cos(self.node_list[i],self.node_list[j]) > THRESHOLD:
                    if self.find_p(i) != self.find_p(j):
                        self.p[self.p[i]] = self.p[j]
            #print num
        #print num
        for i in xrange(len(self.node_list)):
            pa = self.find_p(i)
            if pa in self.group:
                self.group[pa].append(self.node_list[i])
            else:
                self.group[pa] = [self.node_list[i]]
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
                #print " ".join(n[2]).encode('UTF-8'), "     ",
            #print "\n"
            res_json["toc"].append(toc)
        #print json.dumps(res_json)
        return json.dumps(res_json) 

def generate(ids):
    """Generate

    ids: A list of integers. The IDs of related items.
    returns: Learning flow. See $TOP/main_page/README.md
    """
    fa = flow_agent()
    return fa.generate(ids)

if __name__ == '__main__':
    print(generate(search(u'machine learning')))
