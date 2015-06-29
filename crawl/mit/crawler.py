import requests
from bs4 import BeautifulSoup
import json
import os
class mit_parse:
    pre_url = 'http://ocw.mit.edu'
    dept_file = 'dept.txt'
    course_file = 'course_url/'
    def __init__(self, filename):
        self.filename = filename
        self.good = 0
        self.c_num = 0

    def parse_dept(self):
        f = open(self.filename + self.dept_file,'w')
        r = requests.get("http://ocw.mit.edu/courses/find-by-department/")
        soup = BeautifulSoup(r.text)
        for dept in soup.find_all('ul','deptList'):
            tmp = BeautifulSoup(str(dept))
            for li in tmp.find_all('li'):
                f.write(li.a.get('href').strip()+'\n')
        f.close()

    def parse_dept_courses_url(self, dept_url):
        x = []
        url = self.pre_url + dept_url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        
        tmp = soup.find('table','courseList').find_all('a','preview')
        for i,a in enumerate(tmp):
            if i%3 == 0:
                x.append(a.get('href').strip())
        return x

    def parse_courses(self):
        f = open(self.filename + self.dept_file)
        for dept_url in f:
            print 'parse ',dept_url.strip()
            urls = self.parse_dept_courses_url(dept_url.strip())
            f_out = open(self.course_file + dept_url.strip().replace('/','_'), 'w')
            for url in urls:
                f_out.write(url+'\n')
            f_out.close()
        f.close()

    def parse_all_course_json(self):
        res = []
        fout = open('mit.json','w')
        path = 'course_url/'
        filenames = os.listdir(path)
        for filename in filenames:
            if filename =='.gitignore':
                continue
            urls = open(path+filename)
            for url in urls:
                fname = 'json/'+url.strip().replace('/','_')+'.json'
                if os.path.isfile(fname):
                    print('file exist!!!')
                    self.c_num+=1
                    self.good+=1
                    continue
                obj = self.parse_course_json(url.strip())
                print(obj)
                if 'title' in obj:
                    jfile = open(fname,'w')
                    jfile.write(json.dumps(obj))
                    #res.append(obj)
        #fout.write(json.dumps(res))
        #return json.dumps(res)

    def parse_course_json(self,url):
        self.c_num+=1
        print('parse',url)
        res = {}
        try:
            res['title'] = self.parse_course_title(url)
            res['toc'] = self.parse_course_calendar(url)
            res['herf'] = self.pre_url + url
            res['category'] = [url.split('/')[2]]
            if len(res['toc']) > 0:
                self.good += 1
            print('rate: ',self.good,'/',self.c_num)
        except:
            print('page not found!!')
        return res
        

    def parse_course_syllabus(self, url):
        url = self.pre_url + url + '/syllabus'
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        print soup.find_all('div',id='course_inner_section')

    def parse_course_title(self, url):
        ori_url = url
        url = self.pre_url + url
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        titles = soup.find_all('h1',{'class':'title'})
        a = soup.find_all('a')
        w = False
        for aa in a:
            if aa.get('href') == ori_url+'/calendar':
                w = True
        assert w
        assert len(titles)==1
        return titles[0].text

    def parse_course_calendar(self, url):
        res = []
        url = self.pre_url + url + '/calendar'
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        # print(r.text)
        # print(url)
        result = soup.find_all('div',id='course_inner_section')
        for table in result:
            for tr in table.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) == 3 or len(tds) == 4 or len(tds) == 2:
                    res.append(tds[1].text)
                    #print(tds[1].text)
        return res
                    

if __name__ == '__main__':
    hi = mit_parse('mit_')
    # hi.parse_course_calendar('/courses/aeronautics-and-astronautics/16-63j-system-safety-fall-2012')
    # hi.parse_course_calendar('/courses/architecture/4-125a-architecture-studio-building-in-landscapes-fall-2005')
    # hi.parse_course_calendar('/courses/architecture/4-125a-architecture-studio-building-in-landscapes-fall-2005')
    #print(hi.parse_course_title('courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011'))
    #print(json.dumps(hi.parse_course_json('/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011')))
    #print(json.dumps(hi.parse_course_json('/courses/anthropology/21a-225j-violence-human-rights-and-justice-fall-2004')))
    #print(json.dumps(hi.parse_course_json('/courses/mathematics/18-338j-infinite-random-matrix-theory-fall-2004')))
    print(hi.parse_all_course_json())
    # hi.parse_dept()
    # hi.parse_courses()
