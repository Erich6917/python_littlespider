# -*- coding: utf-8 -*-
# @Time    : 2019/3/6 
# @Author  : ErichLee ErichLee@qq.com
# @File    : wifi_local.py
# @Comment : 
#            

import sys
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


def soup_request(urls, coding='utf-8'):
    res = requests.get(urls)
    res.encoding = coding
    return BeautifulSoup(res.text, 'html5lib')


def download_vedio(file_path, path):
    rt = requests.get(path)
    with open(file_path, 'wb') as file_audio:
        file_audio.write(rt.content)


def start():
    url = 'http://172.16.26.201'
    soup = soup_request(url)
    a_list = soup.select("table tbody tr td font a")
    for tag_a in a_list:
        name = u'source/{}.mp3'.format((tag_a.text).replace(" ", ""))
        path = '{}/{}'.format(url,tag_a['href'])
        print name, path
        download_vedio(name, path)


start()