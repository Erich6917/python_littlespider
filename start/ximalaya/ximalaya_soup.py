# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 
# @Author  : LIYUAN134
# @Site    : 
# @File    : ximalaya_soup.py
# @Comment: beautifulSoup 创建工厂
#

import urllib2
from util.logger_util import *
import requests
from bs4 import BeautifulSoup


def request_headers(url, headers):
    try:
        req = requests.get(url, headers=headers)
        return req.text
    except Exception, e:
        errors('REQUEST 获取失败！ ERRMSG > {}'.format(e))
        return ''


#
def request(url):
    try:
        req = requests.get(url)
        return req
    except Exception, e:
        errors('REQUEST 获取失败！ ERRMSG > {}'.format(e))
        return ''


def soup_request(urls, coding='UTF-8'):
    res = requests.get(urls)
    res.encoding = coding

    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(res.text, 'html5lib')
    return rsoup


def soup_urlopen(urls):
    response = urllib2.urlopen(urls)
    data = response.read()

    rsoup = BeautifulSoup(data, 'html5lib')

    return rsoup


def soup_head(urls):
    # 创建请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
               "Accept": "*/*"}
    request = urllib2.Request(urls, headers=headers)
    response = urllib2.urlopen(request)
    data = response.read()
    soup = BeautifulSoup(data, 'lxml')

    return soup
