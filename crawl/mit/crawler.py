import requests
from bs4 import BeautifulSoup
class mit_parse:
    pre_url = 'http://ocw.mit.edu/'
    dept_file = 'dept.txt'
    course_file = 'course_url/'
    def __init__(self, filename):
        self.filename = filename
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
    def parse_course(self):
        f = open(self.filename + self.dept_file)
        for dept_url in f:
            print 'parse ',dept_url.strip()
            urls = self.parse_dept_courses_url(dept_url.strip())
            f_out = open(self.course_file + dept_url.strip().replace('/','_'), 'w')
            for url in urls:
                f_out.write(url+'\n')
            f_out.close()
        f.close()
if __name__ == '__main__':
    hi = mit_parse('mit_')
    hi.parse_dept()
    hi.parse_course()
