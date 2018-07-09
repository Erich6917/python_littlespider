# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 
# @Author  : ErichLee ErichLee@qq.com
# @File    : XingmingTel.py
# @Commment: 
#            

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import json
from bs4 import BeautifulSoup
import time

dict_tel = {
    # u'李': 'http://jia12.com/XingmingKu/?%C0%EE-{0}.html',
    u'王': 'http://jia12.com/XingmingKu/?%CD%F5-{0}.html',
    u'张': 'http://jia12.com/XingmingKu/?%D5%C5-{0}.html',
    u'刘': 'http://jia12.com/XingmingKu/?%C1%F5-{0}.html',
    u'陈': 'http://jia12.com/XingmingKu/?%B3%C2-{0}.html',
}

dict_all = {

    u'杨': 'http://jia12.com/XingmingKu/?%D1%EE-1.html',
    u'黄': 'http://jia12.com/XingmingKu/?%BB%C6-1.html',
    u'赵': 'http://jia12.com/XingmingKu/?%D5%D4-1.html',
    u'周': 'http://jia12.com/XingmingKu/?%D6%DC-1.html',
    u'吴': 'http://jia12.com/XingmingKu/?%CE%E2-1.html',
    u'徐': 'http://jia12.com/XingmingKu/?%D0%EC-1.html',
    u'孙': 'http://jia12.com/XingmingKu/?%CB%EF-1.html',
    u'朱': 'http://jia12.com/XingmingKu/?%D6%EC-1.html',
    u'马': 'http://jia12.com/XingmingKu/?%C2%ED-1.html',
    u'胡': 'http://jia12.com/XingmingKu/?%BA%FA-1.html',
    u'郭': 'http://jia12.com/XingmingKu/?%B9%F9-1.html',
}


def telnet_res(url):
    counter = 0
    while True:
        try:
            res = requests.get(url)
            return res
        except Exception, e:
            if counter >= 10:
                self.errors('放弃连接，尝试连接失败次数>' + int(counter) + '\n')
                return None
            print 'ERROR', counter, e
            time.sleep(3)


def telnet_name_normal():
    for name, url in dict_tel.items():

        file = open(u'source/' + name + '.txt', 'a+')
        for index in range(1, 51):
            telurl = url.format(index)

            print telurl

            res = telnet_res(telurl)

            if None == res:
                continue

            res.encoding = 'gb2312'
            rtmsg = res.text
            # 使用剖析器为html.parser
            rsoup = BeautifulSoup(rtmsg, 'html5lib')
            ta = rsoup.select('#xingmingkuTableID tbody tr td')
            for each in ta:
                msg = each.text
                if msg.startswith(' ') or len(msg) == 0 or len(msg) > 4:
                    pass
                else:
                    file.write(msg + '\n')
            print 'write page success'
        file.close()


if __name__ == '__main__':
    telnet_name_normal()

    # file = open(u'成语-四字.txt', "a")
    # file2 = open(u'成语-超四字.txt', "a")
    # try:
    #     # tel_parse_xiuwenge(1)
    #     telnet_chengyu_noraml()
    # finally:
    #     file.close()
    #     file2.close()
