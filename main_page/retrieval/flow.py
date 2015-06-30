import common
import stemstop
import math
import json
from item_search import search
node_list = []
p = []
node_list = []
threshold = 0.8
group_size = 5
group = {}
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
def find_p(i):
    if p[i] == i:
        return i
    else:
        p[i] = find_p(p[i])
        return p[i]
def generate(ids):
    for _id in ids:
        len_toc = len(common.DOCUMENT_LIST[_id]['toc'])
        for i,topic in enumerate(common.DOCUMENT_LIST[_id]['toc']):
            tmp = stemstop.simpl_stopwords_split(topic.lower())
            tmp = stemstop.stems(tmp)
            #print tmp
            node_list.append(create_node(tmp, float(i)/len_toc, _id))
    #print len(node_list)
    for i in xrange(len(node_list)):
        p.append(i)
    visit = [False for _ in xrange(len(node_list))]
    num = 0
    for i in xrange(len(node_list)):
        #if visit[i]: continue
        for j in xrange(i+1,len(node_list)):
            #if find_p(i) == find_p(j): continue
            num += 1
            if cos(node_list[i],node_list[j]) > threshold:
                visit[j] = True
                if find_p(i) != find_p(j):
                    p[p[i]] = p[j]
        #print num
    #print num
    for i in xrange(len(node_list)):
        pa = find_p(i)
        if pa in group:
            group[pa].append(node_list[i])
        else:
            group[pa] = [node_list[i]]
    res = [(sum(n[1] for n in group[g])/len(group[g]),group[g]) for g in group if len(group[g]) > group_size]
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
    """Generate

    ids: A list of integers. The IDs of related items.
    returns: Learning flow. See $TOP/main_page/README.md
    """
    
if __name__ == '__main__':
    generate(search(u'machine learning'))
    #generate([1,2,3]) 
