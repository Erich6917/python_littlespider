# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : sports.py
# @Commment: 新浪体育版块
#
# coding=utf8

import re

from dbutil.DBNewsUtil import DBNews
from bloom.sina.tools import sinaSoup as bSoup

BASEURL = 'http://sports.sina.com.cn/'


def sport_geturl_roll():
    url_list = []

    soup = bSoup.soup_urlopen(BASEURL)

    # other sports
    othersport = soup.select('.ppcs_l.fl')

    if len(othersport) > 0:

        for index in range(0, len(othersport) - 3):
            alist = othersport[index].select('.list01 a')
            #             print len(alist)
            for a2 in alist:
                # print a2.text, a2.get("href")
                url_list.append(a2.get("href"))

    else:
        print '未定位到[综合体育]'
    return url_list


def sport_geturl_all():
    url_list = sport_geturl_roll()
    print '页面捕获完毕，共计收集到地址：FINAL:', len(url_list)

    p_sports_normal = r'^http://sports.sina.com.cn/.*'

    rdicts = {}
    print '=============开始匹配==============='

    for url in url_list:

        if url in rdicts:
            # 重复url，不再请求
            continue

        if re.match(p_sports_normal, url, re.M):
            vmsg = bSoup.parse_artibody(url)
        else:
            print '暂未匹配该路径', url
            continue

        if vmsg:
            rdicts[url] = vmsg
    print '结果集如下', len(rdicts)

    return rdicts


def telnet_sport_main():
    rdicts = sport_geturl_all()
    scope = 'sports'
    dbnews = DBNews()
    dbnews.save_sina_telnet_result(rdicts, scope)
    print '新浪-体育板块处理完毕！'


def demo():
    import msvcrt
    print ord(msvcrt.getch())


if __name__ == "__main__":
    # demo()
    telnet_sport_main()

    # sports.sport_geturl_all()
