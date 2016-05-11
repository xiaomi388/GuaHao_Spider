import urllib
import urllib2
import re

def get_mid_all(w1,w2,text) :
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    result = pat.findall(text)
    return result

def main() :
    num = 0
    dictionary = {}
    p = open('expertId.txt','a')
    expert_id = []
    url = 'http://www.guahao.com/department/shiftcase/'
    x = input('firstline:')
    y = input('lastline:')
    f = open('deptId.txt','r')
    i = 0
    for q in range(x-1) :
        f.readline()
    while 1 :
        i += 1
        page = 1
        dept_id = f.readline().strip()
        if not dept_id :
            print "finish"
            break
        while 1 :
            geturl = url + dept_id + 'pageNo=' + str(page)
            request = urllib2.Request(geturl)
            try:
                response = urllib2.urlopen(request) 
            except:
                continue
            tmp = get_mid_all('<a target="_blank"  class="name" href="http://www.guahao.com/expert/','\?hospitalId=',response.read())
            if tmp == [] :
                break
            expert_id += tmp
            page += 1
            for ids in tmp :
                try :
                    if dictionary[ids] == 1 :
                        print 'having existed'
                except :
                    dictionary[ids] = 1
                    p.write(ids+'\n')
        print (i + x - 1)
        if i == (y - x + 1) :
            break

if __name__ == '__main__' :
    main()


