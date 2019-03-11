# -*- coding: utf-8 -*-
# @Time    : 2017/9/26 
# @Author  : LIYUAN134
# @File    : joke.py
# @Commment: 笑话收集
#

from bloom.sina.tools import sinaSoup as bSoup
from dbutil.DBNewsUtil import DBNews
from bs4 import BeautifulSoup
import requests

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

JOKEJI_LATELY = 'http://www.jokeji.cn/list.htm'
JOKEJI_HOT_URL_BEFORE = 'http://www.jokeji.cn'


def rao_content_head():
    baseurl = 'http://www.jokeji.cn/hot.asp?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []
    page_start = 5
    page_end = 50
    for page in range(page_start, page_end):
        print '访问进度', page, '/page_end'
        post_param = {'me_page': page}
        return_data = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        data = return_data.text
        ssoup = BeautifulSoup(data, 'html5lib')
        a_list = ssoup.select('.main_14')
        for single in a_list:
            url = single.get('href')
            url = JOKEJI_HOT_URL_BEFORE + url
            # title = single.text
            if p_url.count(url) < 1:
                p_url.append(url)
                # print title, url

    print len(p_url)
    return p_url


def joke_content_school():
    # baseurl = 'http://www.jokeji.cn/list5_1.htm'
    baseurl = 'http://www.jokeji.cn/list5_'
    # url_shcool = 'http://www.jokeji.cn/list5_'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []
    page_start = 1
    page_end = 2
    for page in range(page_start, page_end):
        print '访问进度', page, '/', page_end
        url_shcool = baseurl + str(page) + '.htm'
        print '访问路径', url_shcool
        post_param = {}
        return_data = requests.get(url_shcool, params=post_param, headers=headers, verify=False)
        data = return_data.text
        ssoup = BeautifulSoup(data, 'html5lib')
        a_list = ssoup.select('.list_title a')
        for single in a_list:
            url = single.get('href')
            url = JOKEJI_HOT_URL_BEFORE + url
            # title = single.text
            if p_url.count(url) < 1:
                p_url.append(url)
                # print title, url
                print url

    print len(p_url)
    return p_url


def rao_content():
    url_list = []

    soup = bSoup.soup_urlopen(JOKEJI_LATELY)

    # other sports
    titles = soup.select('.panel .mcon.bt.f14 ul li a')

    if len(titles) > 0:
        for ii in titles:
            urls = JOKEJI_LATELY + ii.get('href')
            # print ii.text, (BASEURL + ii.get('href'))
            url_list.append(urls)
    else:
        print '未定位到[绕口令主页]'
    return url_list


def rao_parse_main(url):
    try:
        soup = bSoup.soup_urlopen(url)
    except BaseException:
        print url, '转soup解析失败'
        return
    dialog = soup.select('#text110')

    msgarr = []
    if len(dialog) > 0:
        # print msg[0].text
        for single in dialog:
            msgarr.append(single.text)
            # return msg[0].text
        return "".join(msgarr)


def rao_geturl_all():
    # url_list = rao_content()
    url_list = []
    url_shool = joke_content_school()
    url_list.extend(url_shool)
    # url_hot = rao_content_head()
    print '页面捕获完毕，共计收集到地址：FINAL:', len(url_list)

    rdicts = {}
    for url in url_list:
        vmsg = rao_parse_main(url)
        if vmsg is not None:
            rdicts[url] = vmsg
        else:
            print 'URL请求内容为空 跳过', url
    print '结果集如下', len(rdicts)
    # for k, v in rdicts.items():
    #     print k, v

    return rdicts


def rao_telnet_main():
    rdicts = rao_geturl_all()
    scope = 'joke'
    dbnews = DBNews()
    dbnews.save_sina_telnet_result(rdicts, scope)

    print '笑话收集完成！'


if __name__ == "__main__":
    # rao_geturl_all()
    rao_telnet_main()
    # rao_parse_main('http://www.jokeji.cn/jokehtml/mj/20091106004033.htm')
    # joke_content_school()
    # rao_content_head()
