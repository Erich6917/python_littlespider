# -*- coding: utf-8 -*-
# @Time    : 2018/10/25 
# @Author  : ErichLee ErichLee@qq.com
# @File    : RT_spider.py
# @Comment : 
#            

import sys
import re
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


def request_first():
    url = 'http://finance.sina.com.cn/world/'  # 国际财经
    data = requests.get(url)
    print data.text


def request_sina():
    url = 'http://finance.sina.com.cn/world/'  # 国际财经
    p_url = []
    data = requests.get(url)
    regex = 'href="(https?://(?:finance.sina.com.cn|blog.sina.com.cn)/[^"]+)'
    result = re.findall(regex, data.text)
    for item in result:
        url = item
        print url
        if url:
            p_url.append(url)
    return p_url


def beautiful_sina():
    url = 'http://finance.sina.com.cn/world/'
    res = requests.get(url)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text, 'html5lib')
    ta = soup.select('body .wrap .part-c.clearfix li a')
    for each in ta:
        print each.text


def rk_create(im, im_type, timeout=60):
    params = {
        'typeid': im_type,
        'timeout': timeout,
    }
    files = {'image': ('a.jpg', im)}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
               "Accept": "*/*"}
    r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=headers)
    return r.json()
