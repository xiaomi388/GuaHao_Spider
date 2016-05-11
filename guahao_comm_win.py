# -*- coding:utf-8 -*-
import urllib
import urllib2
import json
import re
import time
import cookielib
from openpyxl import Workbook
from openpyxl import load_workbook
import os



hospital_list = []
filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


def login():
    global cookie
    global opener
    url = 'http://www.guahao.com/user/login'
    result = opener.open(url)
    img_url = 'http://www.guahao.com/validcode/genimage/1'
    img = opener.open(img_url)
    img_file = file('captcha.jpg','wb')
    img_file.write(img.read())
    img_file.close()
    validCode = raw_input('input the validCode:')
    data = urllib.urlencode({
            'method' : 'dologin',
            'target' : '/',
            'loginId' : '13226587897',
            'password' : 'e7eba97573d17f13d229bec4fb0e3628',
            'validCode' : validCode
            })
    result = opener.open(url,data)
    cookie.save(ignore_discard=True,ignore_expires=True)
    try:
        tmp = get_mid('<span class="gi gi-error">','span>',result.read())
        print 'Error:Maybe you have entered a wrong validCode,please close the window and try again'
        time.sleep(100)
    except:
        print 'Login successfully!Start getting information now!'
        
class comment :
    def __init__(self) :
        self.name = 'unknown'
        self.ill = 'unknown'
        self.manyi = 'unknown'
        self.content = 'unknown'
        self.time = 'unknown'
        self.source = 'unknown'
        self.patient = 'unknown'
    def get_all(self) :
        tmp =  self.patient + '&' +  self.ill + '&' + self.manyi + '&' + self.content + '&' + self.time + '&' + self.source + '&' + self.name
        return tmp

def clear(s) :
    s = s.replace(' ','')
    s = s.replace('	','')
    s = s.replace('\n','')
    s = s.replace('\r','')
    s = s.replace('<span>','')
    s = s.replace('</span>','')
    s = s.replace('<strong>','')
    s = s.replace('</strong>','')
    s = s.replace('<p>','')
    s = s.replace('</p>','')
    s = s.replace('&nbsp;',' ')
    return s


def get_mid(w1,w2,text):
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    result = pat.findall(text)
    return result[0]

def get_mid_all(w1,w2,text):
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    result = pat.findall(text)
    return result

def get_mid_op(w1,w2,text,i):
    pat = re.compile(w1+'(.*?)'+w2,re.S)
    result = pat.findall(text)
    return result[i]

qform = {
    'pageNo' : '',
    'sign' : '',
    'timestamp' : ''
    }

def get_info(url,i):
    global opener
    global qform
    def connect(url):
       response = opener.open(url)
       return response.read()
    def get_form(text):
       w1 = '<form name="qPagerForm" action="">'
       w2 = '<div'
       tmp = get_mid(w1,w2,text)
       qform['sign'] = get_mid('name="sign" value="','"/>',tmp)
       qform['timestamp'] = get_mid('name="timestamp" value="','"/>',tmp)
            
    def turnOver(no):
       qform['pageNo'] = no
       data = urllib.urlencode(qform)
       #url2 = 'http://www.guahao.com/commentslist/h-125336754304601000/1-0' + '?' + data
       url2 = url + '?' + data
       return connect(url2)
    def get_need(text) :
        tmp = {}
        w1 = '<div class="photo">'
        w2 = '</div>'
        temp2 = get_mid(w1,w2,text)
        w1 = 'alt="'
        w2 = '"'
        temp2 = get_mid(w1,w2,temp2)
        w1 = '<div class="text">'
        w2 = '</div>'
        temp = get_mid_all(w1,w2,text)
        for a in range(len(temp)):
            temp[a] = clear(temp[a])
            temp[a] = temp[a].replace('<spanclass="summary">','')
            temp[a] = temp[a].replace('</span>','')
        tmp['content'] = temp
        w1 = '<span>来源：'
        w2 = '</span>'
        temp = get_mid_all(w1,w2,text)
        for a in range(len(temp)) :
            temp[a] = clear(temp[a])
        tmp['source'] = temp
        w1 = '<p class="disease">'
        w2 = '</p>'
        temp = get_mid_all(w1,w2,text)
        for a in range(len(temp)) :
            w1 = '<span>'
            w2 = '</span>'
            if tmp['source'][a] == '医院就诊':
                temp[a] = get_mid(w1,w2,temp[a])
            else :
                temp[a] = '无'
        tmp['ill'] = temp
        w1 = '<p class="attitude">'
        w2 = '</p>'
        temp = get_mid_all(w1,w2,text)
        for a in range(len(temp)) :
            w1 = '<strong>'
            w2 = '</strong>'
            temp[a] = get_mid(w1,w2,temp[a])
            temp[a] = clear(temp[a])
        tmp['manyi'] = temp 

        w1 = '<div class="info">'
        w2 = '/span>'
        test = get_mid(w1,w2,text)
        temp = get_mid_all(w1,w2,text)
        tmp['name'] = []
        for a in range(len(temp)-1) :
            w1 = '<span>'
            w2 = '<'
            temp[a] = get_mid(w1,w2,temp[a])
            temp[a] = clear(temp[a])
            tmp['name'].append(temp2)
        temp.pop()
        tmp['time'] = temp 
        w1 = '<div class="user">'
        w2 = '</div>'
        temp = get_mid_all(w1,w2,text)
        for a in range(len(temp)) :
            w1 = '<p>'
            w2 = '</p>'
            temp[a] = get_mid(w1,w2,temp[a])
            temp[a] = clear(temp[a])
        tmp['patient'] = temp
        return tmp
        
    if i == 1 :
        text = connect(url)
        get_form(text)
    else :
        text = turnOver(i)
        get_form(text)
    tmp = get_need(text)
    return tmp

def get_time() :
    return str(time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())))

def main() :
    log = file('log.txt','w')
    log.write('上一次程序开始于' + get_time() + '\n')
    f = open('expertId.txt')
    txt_data = open('data_comment.txt','a')
    x = input('first line:')
    y = input('last line:')
    login()
    for x1 in range(x-1):
        f.readline()
    for x1 in range(y-x+1):
        expertid = f.readline().strip()
        i = 1
        while 1 :
            try:
                tmp = get_info('http://www.guahao.com/commentslist/e-'+expertid+'/1-0',i)
            except:
                temp2 =  '第' + str(x1+x) + '位医生信息已经读取完毕'
                print temp2.decode('utf-8').encode('gb2312')
                break
#            tmp = get_info('http://www.guahao.com/commentslist/e-07aef26c-28de-4c4f-af98-b2c49e1bcf20000/1-0',i)
            if len(tmp['patient']) == 0 :
                temp2 =  '第' + str(x1+x) + '位医生信息已经读取完毕'
                print temp2.decode('utf-8').encode('gb2312')
                break
            for q in range(len(tmp['patient'])) :
                hospital_list.append(comment())
                num = len(hospital_list) - 1
                hospital_list[num].content = tmp['content'][q]
                hospital_list[num].name = tmp['name'][q]
                hospital_list[num].source = tmp['source'][q]
                hospital_list[num].time = tmp['time'][q]
                hospital_list[num].patient = tmp['patient'][q]
                hospital_list[num].ill = tmp['ill'][q]
                hospital_list[num].manyi = tmp['manyi'][q]
                temp2 = '已抓取该医生' + str((5*(i-1))+q+1) + '条信息'
                txt_data.write('\n' + str(hospital_list[num].get_all()))
                print temp2.decode('utf-8').encode('gb2312')
            i += 1
        sum_log = get_time() + '  ' + '获取了第' + str(x+x1) + '位医生的信息' + '\n'
        log.write(sum_log)
    txt_data.close()
    f.close()
    log.close()
if __name__ == '__main__' :
    main()

