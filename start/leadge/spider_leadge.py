# -*- coding: utf-8 -*-
# @Time    : 2019/5/15
# @Author  : ErichLee ErichLee@qq.com
# @File    : spider_leadge.py
# @Comment :
#

import sys
import requests
import random
from bs4 import BeautifulSoup
from util.logger_util import *
from util.file_check_util import *
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def telnet(url):
    try:
        rt = requests.get(url)  # , headers=hd
        # requests.encoding = 'utf-8'
        # print rt.text
        return BeautifulSoup(rt.content, 'html5lib')
    except Exception as e:
        errors('访问失败！{}'.format(e))


def start_leadge():
    fid_list = ['12012134', '12012138', '12012139', '12012145', '12012143', '12012144', '12012146', '12012147']

    for fid_id in fid_list:
        # fid_id = 12012144
        url = 'http://www.leadge.com/news_list/list_{}.html'.format(fid_id)
        soup = telnet(url)

        # s1 find page size
        page_msg = soup.select_one('div#pager1 table tbody tr td.paginator').text
        page_max = int(re.search(u'[0-9]+/([0-9]+)页', page_msg).group(1))
        print 'max_size', page_max

        # s2

        href_list = []
        href_list.append(url)
        if page_max > 1:
            url_page = 'http://www.leadge.com/news_list/list.aspx?fid={}&page={}'
            for index in range(2, page_max + 1):
                href = url_page.format(fid_id, index)
                href_list.append(href)

        rt_list = []
        for href in href_list:
            soup = telnet(href)
            a_list = soup.select('div#newslist_pcon div.newsshowsty dl dt a')
            for h_tag in a_list:
                title, href_target = h_tag['title'], \
                                     'http://www.leadge.com/news_list/{}'.format(h_tag['href'])

                rt_list.append('{}\t{}'.format(title, href_target))

        with open('url.txt', 'a+') as file:
            file.writelines('\n'.join(rt_list))


# start_leadge()


def start_parse_url():
    with open('url.txt', 'a+') as file_url:
        url_list = file_url.readlines()
    for each in url_list:
        title, href = each.split('\t')[0], each.split('\t')[1].strip()
        print title, href

        # title, href = u'在项目管理中面对面交流最重要', 'http://www.leadge.com/news_list/68250.html'
        # title = u'在项目管理中面对面交流最重要'
        soup = telnet(href)
        span_list = soup.select('div.blkCont span')
        text_list = [msg.text for msg in span_list]
        rt_msg = '\n'.join(text_list)

        with open('source/{}.txt'.format(title).decode('utf-8'), 'a+') as rt_file:
            rt_file.writelines(rt_msg)


start_parse_url()
