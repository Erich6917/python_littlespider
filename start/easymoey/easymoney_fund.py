# -*- coding: utf-8 -*-
# @Time    : 2019/1/28
# @Author  : ErichLee ErichLee@qq.com
# @File    : easymoney_fund.py
# @Comment :
#

import json
import sys
from bs4 import BeautifulSoup
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

'''
    天天基金 http://fund.eastmoney.com
'''


def soup_request(urls, coding='gbk'):
    res = requests.get(urls)
    res.encoding = coding

    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(res.text, 'html5lib')
    return rsoup


def parse_news_normal(urls, coding='utf-8'):
    try:
        soup = soup_request(urls, coding)
        body = soup.select('#ContentBody')
    except Exception, e:
        print 'Soup 解析失败', urls, e
        return None

    rarr = []
    if len(body) > 0:
        pmsg = body[0].select('p')
        for msg in pmsg:
            rarr.append(msg.text)
    else:
        print 'find artibody failed', urls
        return None
    rmsg = ''.join(rarr)
    return rmsg


def save_msg(rt_href):
    file_cjjztyj = open(u'基金滚动20190128.txt', 'a+')
    for href in rt_href:
        print 'telnet  ', href
        msg = parse_news_normal(href)
        if msg:
            file_cjjztyj.write(msg + '\n')
    file_cjjztyj.close()


def get_url_cjjztyj():
    url_list = [  # 'http://fund.eastmoney.com/a/cjjztyj.html', 'http://fund.eastmoney.com/a/cjjztyj_2.html',
        # 'http://fund.eastmoney.com/a/cjjgjfx.html',
        # 'http://fund.eastmoney.com/a/cjjgjfx_2.html',
        # 'http://fund.eastmoney.com/a/cjjgjfx_3.html',
        # 'http://fund.eastmoney.com/a/cjjgjfx_4.html',


        # 'http://fund.eastmoney.com/a/cjjtzcl.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_2.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_3.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_4.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_5.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_6.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_7.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_8.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_9.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_10.html',
        # 'http://fund.eastmoney.com/a/cjjtzcl_11.html'

        'http://roll.eastmoney.com/fund.html',
        'http://roll.eastmoney.com/fund.html_1',
    ]
    rt_href = []
    for href in url_list:
        soup = soup_request(href)
        a_list = soup.select('body  div.infos ul li a')
        for a in a_list:
            href, title = 'http://fund.eastmoney.com/a/' + a['href'], a['title']
            rt_href.append(href)
    return rt_href


def runk_roll(index):
    baseurl = 'http://roll.eastmoney.com/list?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Accept": "*/*"}

    post_param = {'count': 40, 'type': 10, 'type': 'fund', 'pageindex': index}  # 产经
    req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
    rtjson = json.loads(req.text)

    for each in rtjson:
        print each['url']

    return [each['url'] for each in rtjson]


def start_fund_roll():
    for index in range(40):
        rt_href = runk_roll(index)
        save_msg(rt_href)


def start_fund_cjjztyj():
    start_fund_cjjztyj()
    href = 'http://fund.eastmoney.com/a/20171106799044058.html'

    msg = parse_news_normal(href)
    print msg


def  dump():
    list =["key:",""]

start_fund_roll()
