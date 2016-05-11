import urllib
import urllib2
import re

def get_mid_all(w1,w2,text) :
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    result = pat.findall(text)
    return result

dept_id = []
i = 0
f = open('hosptialId.txt','r')
url = 'http://www.guahao.com/hospital'
values = {}
values['pageNo'] = 1
while 1 :
    i += 1
    hospital_id = f.readline().strip()
    if not hospital_id:
        print "finish"
        break
    data = urllib.urlencode(values)
    geturl = url + '/' + hospital_id  
    request = urllib2.Request(geturl)
    response = urllib2.urlopen(request)
    tmp = get_mid_all('http://www.guahao.com/department/','?isStd=',response.read())
    dept_id += tmp
    print i 

sum1 = ''
q = open('deptId.txt','w')
for i in dept_id :
    sum1 += i
    sum1 += '\n'
q.write(sum1)
f.close()
q.close()
    


