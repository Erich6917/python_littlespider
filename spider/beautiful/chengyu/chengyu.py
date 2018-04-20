# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : chengyu.py
# @Commment: 成语大全
#

import re
import sys

import requests
import json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('UTF-8')


def chengyu_getcount(types):
    total = {
        '911cha': 20,
        'xiuwenge': 111
    }.get(types, 0)
    return total


def tel_parse_991cha(page):
    # url = 'https://chengyu.911cha.com/zishu_4_p2.html'
    url_head, url_end = \
        'https://chengyu.911cha.com/zishu_4_p', '.html'
    url = url_head + str(page) + url_end
    print url
    res = requests.get(url)
    res.encoding = 'UTF-8'

    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(res.text, 'html5lib')
    ta = rsoup.select('body .mcon li a')
    print len(ta)
    for each in ta:
        msg = each.text + '\n'
        file.write(msg)


def tel_parse_xiuwenge(page):
    # url = 'https://chengyu.911cha.com/zishu_4_p2.html'
    print 'PAGE:', page
    url_head, url_end = \
        'http://chengyu.xiuwenge.com/daquan/map', '.html'
    url = url_head + str(page) + url_end
    # url = 'http://chengyu.xiuwenge.com/daquan/'
    res = requests.get(url)
    res.encoding = 'gb2312'
    rtmsg = res.text
    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(rtmsg, 'html5lib')
    ta = rsoup.select('#main2 .cydaquanlist li a')
    for each in ta:
        msg = each.text
        msg = msg.decode('utf-8') + '\n'

        if len(msg) == 5:
            file.write(msg)
            continue
        file2.write(msg)


def telnet_chengyu_noraml():
    # steps = 1
    # https://chengyu.911cha.com/zishu_4_p1.html
    # https://chengyu.911cha.com/zishu_4_p20.html
    # 911cha
    # https://chengyu.911cha.com/zishu_4_p1.html    p1-p20
    type_list = ['911cha']
    type_list = ['xiuwenge']

    for types in type_list:
        total = chengyu_getcount(types)
        # for page in range(1, total + 1):
        #     tel_parse_991cha(page)
        for page in range(1, total + 1):
            tel_parse_xiuwenge(page)


def clean_4_gk2312():
    # '�'
    # f = open("c:\\1.txt", "r")
    #
    # lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    #
    # for line in lines
    #
    #     print line
    """
        四字成语的清理
    """
    file = open(u'成语-四字.txt', "ab+")
    file2 = open(u'成语-四字-乱码.txt', "ab+")
    file3 = open(u'成语-四字-全部.txt', "ab+")
    try:
        line = file.readline()  # 调用文件的 readline()方法
        while line:
            msg = line
            if '�' in line:
                file2.write(msg)
            else:
                file3.write(msg)

            line = file.readline()
    finally:
        file.close()
        file2.close()
        file3.close()


def clean_l4_gk2312():
    # '�'
    """
        超四字成语的清理
    """
    file = open(u'成语-超四字.txt', "ab+")
    file2 = open(u'成语-超四字-乱码.txt', "ab+")
    file3 = open(u'成语-超四字-全部.txt', "ab+")
    try:
        line = file.readline()  # 调用文件的 readline()方法
        while line:
            msg = line
            if '�' in line:
                file2.write(msg)
            else:
                file3.write(msg)

            line = file.readline()
    finally:
        file.close()
        file2.close()
        file3.close()


if __name__ == '__main__':
    # tel_parse_start()
    # tel_parse_xiuwenge(2)

    # clean_4_gk2312()
    # clean_l4_gk2312()

    file = open(u'成语-四字.txt', "a")
    file2 = open(u'成语-超四字.txt', "a")
    try:
        # tel_parse_xiuwenge(1)
        telnet_chengyu_noraml()
    finally:
        file.close()
        file2.close()
