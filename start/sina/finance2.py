# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : finance.py
# @Commment: 新浪财经板块
#

import re
import sys

import requests
import json
import socket
socket.setdefaulttimeout(5)

import dateCheckUtil as dateUtil
from bloom.sina.tools import sinaSoup as bSoup

# from dbutil.DBNewsUtil import DBNews

reload(sys)
sys.setdefaultencoding('UTF-8')


# dbnews = DBNews()


def _finance_geturl_roll():
    """
    财经滚动  解析json内容
    访问地址 http://finance.sina.com.cn/roll/

    """
    baseurl = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?'
    'spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&r=0.9330196594434315'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               # "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []

    for page in range(1, 22):
        # for page in range(1):
        post_param = {'col': '43', 'page': page}
        return_data = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        data = return_data.text

        #         print data
        result = re.findall('{channel : {title : (.+?),id : .*},title : "(.*)",url : "(.*)",type.*,time :(.*)},', data)
        for item in result:
            url = item[2]
            # print chardet.detect(item[1])
            # print item[1], '>', item[2], '>', item[3]
            if url:
                p_url.append(url)

    print len(p_url)
    return p_url


def _finance_geturl_world():
    """
    国际财经，只从首页上获取，其他为
    访问地址 http://finance.sina.com.cn/

    """
    baseurl = 'http://finance.sina.com.cn/world/'
    p_url = []

    data = requests.get(baseurl)  # print data
    regex = 'href="(https?://(?:finance.sina.com.cn|blog.sina.com.cn)/[^"]+)'
    result = re.findall(regex, data.text)
    for item in result:
        url = item
        print url
        # print chardet.detect(item[1])
        # print item[1], '>', item[2], '>', item[3]
        if url:
            p_url.append(url)
    return p_url


def _finance_geturl_china(start=1, end=2):
    """
    国内财经，5sheet,5分页,10每页
    访问地址 http://finance.sina.com.cn/china/

    """
    baseurl = 'http://feed.mix.sina.com.cn/api/roll/get?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               # "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []

    print 'page:', start, end
    for page in range(start, end):
        # post_param = {'pageid': '155', 'num': 10, 'page': page, 'lid': 1686}  # 1686 财经-国内
        # pageid 155 财经国内,lid 1686 > 国内滚动,1687>宏观经济,1688>地方经济, 1690》金融新闻,1689>部委动态
        post_param = {'pageid': '164', 'num': 10, 'page': page, 'lid': 1693}  # 产经
        req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        rtjson = json.loads(req.text)
        result = rtjson['result']
        data = result['data']
        # if True:
        #     # print rtjson
        #     print 'total:', result['total']
        #     return
        for ii in data:
            # print ii['url']
            p_url.append(ii['url'])
    return p_url


def finance_parse_start(url_list):
    """

    :param url_list: 需要解析的URL
    :return: 返回KEY > URL，Value > 捕获内容格式的信息
    """
    if len(url_list) > 0:
        print '页面捕获完毕，本次收集到地址：FINAL:', len(url_list)
    else:
        print '没有需要解析的URL'
        return

    p_blog = r'https?://blog.sina.com.cn/s/.*'  # sina blog

    p_finance = r'https?://finance.sina.com.cn/.*'  # sina finace normal type

    rdicts = {}
    num_exist = 0
    print '=============开始匹配==============='

    for url in url_list:
        print url
        if url in rdicts:
            # 重复url，不再请求
            continue
        try:

            # urlparam = {"news_url": url}
            # isexist = dbnews.isexist_newsmsg(urlparam)
            # if isexist:
            #     print '地址已经存库', url
            #     num_exist += 1
            #     continue

            if re.match(p_finance, url, re.M):
                vmsg = finance_parse_top_cj(url)
            elif re.match(p_blog, url, re.M):
                vmsg = finance_parse_top_blog(url)
            else:
                print '暂未匹配该路径', url
                continue
            if vmsg:
                rdicts[url] = vmsg
                if len(rdicts) % 50 == 0:
                    print '已经获取记录数', len(rdicts), dateUtil.currDateFormate()
        except Exception, e:
            print '解析失败：', url, ':', e
            continue
    print '本次采集数量：', len(rdicts)

    return rdicts


# 新浪博客内容获取
def finance_parse_top_blog(url):
    return bSoup.parse_top_blog(url)


# 财经首页内容获取
def finance_parse_top_cj(url):
    return bSoup.parse_artibody(url)


'''获取新浪新闻根据请求地址获取信息入库 170905
'''


def telnet_finance_main():
    # finance main save db
    pstart = 1
    steps = 10
    # 300 -900 6500
    file_finance = open('finance_20190114.txt', 'a+')
    while pstart < 50:
        pend = pstart + steps
        print 'start:', dateUtil.currDateFormate()
        url_list = []
        url_list.extend(_finance_geturl_china(pstart, pend))  # 国内财经

        rdicts = finance_parse_start(url_list)
        scope = 'finance'
        # dbnews.save_sina_telnet_result(rdicts, scope)
        for rUrl, rMsg in rdicts.items():
            print rMsg
            file_finance.write(rMsg + '\n')
        file_finance.flush()

        print 'end:', dateUtil.currDateFormate()

        pstart += steps

    # url_list = []
    # url_list.extend(_finance_geturl_roll())  # roll
    # url_list.extend(_finance_geturl_world())  # 国际财经首页
    # url_list.extend(_finance_geturl_china(start, end))  # 国内财经

    # rdicts = finance_parse_start(url_list)
    # scope = 'finance'
    # dbnews.save_sina_telnet_result(rdicts, scope)
    print '新浪-财经板块处理完毕！'


if __name__ == "__main__":
    print 'start:', dateUtil.currDateFormate()
    telnet_finance_main()
    print 'end:', dateUtil.currDateFormate()
    # _finance_geturl_china()
