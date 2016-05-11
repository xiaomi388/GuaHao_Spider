# -*- coding:utf-8 -*-
import urllib
import re
import urllib2
import json

hospital_id = []
pi = 1
suma = 1
values = {}
#values['sort'] = 'region_sort'
values['ipIsShanghai'] = 'False'
#values['fg'] = '0'
#values['c'] = '不限'
#values['ht'] = 'all'
#values['q'] = ''
#values['hk'] = ''
#values['p'] = '全国'
#values['ci'] = 'all'
#values['o'] = 'all'
#values['hl'] = 'all'
url = 'http://www.guahao.com/hospital/areahospitals'

def get_mid_all(w1,w2,text) :
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    result = pat.findall(text)
    return result

for i in range(34) :
    if i == 0 or i == 26 or i == 28 :
        continue
    else :
        values['pi'] =  i
        page = 1
        while(1) :
            values['pageNo'] = page
            data = urllib.urlencode(values)
            geturl = url + '?' + data
            request = urllib2.Request(geturl)
            response = urllib2.urlopen(request)
            tmp = get_mid_all('<a class="a" href="http://www.guahao.com/hospital/','" target="_blank"',response.read())
            if tmp == [] :
                break
            hospital_id += tmp
            page += 1
            print suma
            suma += 1
sum_id = ''
f = file('hosptialId.txt','w')
for i in hospital_id :
    sum_id += i 
    sum_id += '\n'
f.write(sum_id)
f.close()

    

