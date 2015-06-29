import os
import json
import re
fout = open('mit.json','w')
filenames = os.listdir('json/')
res = []
_id = 0
for fname in filenames:
    f = open('json/'+fname)
    obj = json.loads(f.next())
    obj['id'] = _id
    _id += 1
    for i in range(len(obj['toc'])):
        s = obj['toc'][i].replace('\n',' ')
        s = s.replace('\r',' ')
        s = re.sub('\ +',' ',s)
        obj['toc'][i] = s
    res.append(obj)
    #print(obj)
fout.write(json.dumps(res))
fout.close()
