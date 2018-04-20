# -*- coding: utf-8 -*-
# @Time    : 2017/12/27 
# @Author  : LIYUAN134
# @File    : qsbk_demo.py
# @Commment: 修饰百科
#

# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
from bs4 import BeautifulSoup



def demo1():
    page = 1
    url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    cookie = '_xsrf=2|1113665b|32757988ad1b56bc339f7c3a061f977a|1514338646; _qqq_uuid_="2|1:0|10:1514338647|10:_qqq_uuid_|56:ZDAzN2FkMjkwNGY3YWZkNThiYzU0YmYyYTM0YzQxYTljNDNmZjJmYQ==|0c84bc929dd03eddf271455e7582aa64e807f0b7e861762e91f286974ff911d1"; ADEZ_BLOCK_SLOT=FUCKIE; ADEZ_ST=FUCKIE; ADEZ_Source=www.qiushibaike.com/hot/; _gat=1; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1514338640,1514339590; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1514339680; _ga=GA1.2.1660563119.1514338645; _gid=GA1.2.54198147.1514338645; ADEZ_ASD=1; ADEZ_PVC=1026761-10-jbovw5h7'
    headers = {'User-Agent': user_agent, 'Cookie': cookie}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        print response.read()
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


def demo2():
    # -*- coding:utf-8 -*-

    page = 1
    url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    cookie = '_xsrf=2|1113665b|32757988ad1b56bc339f7c3a061f977a|1514338646; _qqq_uuid_="2|1:0|10:1514338647|10:_qqq_uuid_|56:ZDAzN2FkMjkwNGY3YWZkNThiYzU0YmYyYTM0YzQxYTljNDNmZjJmYQ==|0c84bc929dd03eddf271455e7582aa64e807f0b7e861762e91f286974ff911d1"; ADEZ_BLOCK_SLOT=FUCKIE; ADEZ_ST=FUCKIE; ADEZ_Source=www.qiushibaike.com/hot/; _gat=1; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1514338640,1514339590; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1514339680; _ga=GA1.2.1660563119.1514338645; _gid=GA1.2.54198147.1514338645; ADEZ_ASD=1; ADEZ_PVC=1026761-10-jbovw5h7'
    headers = {'User-Agent': user_agent, 'Cookie': cookie}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        # pattern = re.compile('&lt;div.*?author"&gt;.*?&lt;a.*?&lt;img.*?&gt;(.*?)&lt;/a&gt;.*?&lt;div.*?' +
        #                      'content"&gt;(.*?)&lt;!--(.*?)--&gt;.*?&lt;/div&gt;(.*?)&lt;div class="stats.*?class="number"&gt;(.*?)&lt;/i&gt;',
        #                      re.S)
        rsoup = BeautifulSoup(content, 'html5lib')
        divs = rsoup.select('.author.clearfix')
        for div in divs:
            if div.select('h2'):
                print 'author:', div.select('h2')[0].text

        msgs = rsoup.select('.content')
        for msg in msgs:
            print msg.text
            # print div
            # if div.select('.content'):
            #     print 'bingo'
            #     print div.select('.content')[0].text
                # items = re.findall(pattern, content)
                # print items
                # for item in items:
                #     haveImg = re.search("img", item[3])
                #     if not haveImg:
                #         print item[0], item[1], item[2], item[4]
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


demo2()
