# -*- coding: utf-8 -*-
# @Time    : 2018/8/16
# @Author  : ErichLee ErichLee@qq.com
# @File    : zhufuyu_url.py
# @Comment :
#

import sys
import requests
import re

import time

from util.logger_util import *
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


def telnet(url):
    try:
        rt = requests.get(url)
        requests.encoding = 'utf-8'
        return rt.content
    except Exception as e:
        errors('访问失败！{}'.format(e))


def download():
    file_url = open('url.txt', 'r')
    url_list = file_url.readlines()
    for url in url_list:
        url = url.strip()
        html = telnet(url)
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(2)
        arr_url = parse_page_msg(soup)
        if arr_url:
            infos("TELNET {}, > {}".format(url, len(arr_url)))
            save_url(arr_url)
        else:
            infos("TELNET  EMPTY {} ".format(url))


def start():
    url_obj = [
        'http://www.zk008.com/duanxin/lb-34.html',
        'http://www.zk008.com/duanxin/lb-35.html',
        'http://www.zk008.com/duanxin/lb-36.html',
        'http://www.zk008.com/duanxin/lb-37.html',
        'http://www.zk008.com/duanxin/lb-38.html',
        'http://www.zk008.com/duanxin/lb-53.html',
        'http://www.zk008.com/duanxin/lb-54.html',
        'http://www.zk008.com/duanxin/lb-163.html',
    ]
    rt_list = []
    for url in url_obj:
        html = telnet(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            page_total = parse_gage_total(soup)
            arr_url = get_full_url(page_total, url)
            rt_list.extend(arr_url)
        time.sleep(2)

    # print rt_list
    with open('url.txt', 'w') as file:
        for each in rt_list:
            msg = '{}\n'.format(each)
            file.write(msg)


def get_full_url(page_total, url):
    rt_url = []
    if page_total > 1:
        for index in range(2, page_total + 1):
            page = 'p{}'.format(index)
            page_replace = '-{}.html'.format(page)
            url_replace = url.replace('.html', page_replace)
            rt_url.append(url_replace)
    rt_url.append(url)
    return rt_url


def parse_page_msg(soup):
    msg_list = soup.select('div.new_zuid2 div div div div div div div div span')
    # for msg in msg_list:
    #     print msg.text
    if msg_list:
        return [msg.text for msg in msg_list]


def parse_gage_total(soup):
    try:
        rt_msg = soup.select('div.page em')[0]
        total = int(re.sub('[^0-9]', '', rt_msg.text))
    except Exception, e:
        errors('页面获取失败{}'.format(e))
        return

    page_max = 20

    if total % page_max == 0:
        page_total = total / page_max
    else:
        page_total = total / page_max + 1
    infos('total > {} , page > {}'.format(total, page_total))
    return page_total


def save_url(arr_list):
    with open('result.txt', 'a') as file:
        for url in arr_list:
            msg = '{}\n'.format(url)
            file.write(msg)


# start()
download()
