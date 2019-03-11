# -*- coding: utf-8 -*-
# @Time    : 2017/9/18 
# @Author  : LIYUAN134
# @Site    : 
# @File    : sinaSoup.py
# @Commment: beautifulSoup 创建工厂
#

import urllib2

import requests
from bs4 import BeautifulSoup


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


# sinasoup 解析类型一 artibody》p
def parse_artibody(urls):
    try:
        soup = soup_urlopen(urls)

        body = soup.select('#artibody')
        if not body:
            body = soup_head(urls).select('#artibody')
    except Exception, e:
        print 'Soup 解析失败', urls, e
        return None

    rarr = []
    if len(body) > 0:
        pmsg = body[0].select('p')
        for msg in pmsg:
            #                 print msg.text
            rarr.append(msg.text)
    else:
        print 'find artibody failed', urls
        return None
    rmsg = ''.join(rarr)
    return rmsg


def parse_content(urls):
    try:
        soup = soup_urlopen(urls)

        body = soup.select('#artibody')
        if not body:
            body = soup_head(urls).select('#artibody')
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
    print rmsg
    return rmsg


def parse_tech_normal(urls):
    try:
        soup = soup_urlopen(urls)

        body = soup.select('#artibody')
        if not body:
            body = soup_head(urls).select('#artibody')
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
    # print rmsg
    return rmsg


def parse_news_normal(urls):
    try:
        soup = soup_urlopen(urls)

        body = soup.select('#article')
        if not body:
            body = soup_head(urls).select('#articleContent')
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


def parse_news_old_normal(urls):
    try:
        soup = soup_urlopen(urls)

        body = soup.select('#J_Article_Wrap #artibody')
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


def parse_news_art_normal(urls):
    try:
        soup = soup_urlopen(urls)

        body = soup.select('#J_Article_Wrap #artibody')
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


# url = 'http://news.sina.com.cn/s/2014-04-11/093929911184.shtml'
# url = 'http://cul.news.sina.com.cn/stickynews/2017-11-14/doc-ifynshev5940656.shtml'
# url = 'http://news.sina.com.cn/s/2018-03-12/doc-ifysevxp7028104.shtml'
# url = 'http://news.sina.com.cn/c/2018-04-12/doc-ifyuwqez9468537.shtml'
# print parse_news_normal(url)


# titles, msgs, times = parse_artibody_details()
# print titles
# print msgs
# print times


# 新浪博客正文获取
def parse_top_blog(url):
    #     url = 'http://blog.sina.com.cn/s/blog_6fe7ef8d0102xe9z.html'
    soup = soup_urlopen(url)
    body = soup.select('#articlebody #sina_keyword_ad_area2')
    rarr = []
    if len(body) > 0:
        pmsg = body[0].select('p')
        for msg in pmsg:
            rarr.append(msg.text)
    else:
        print 'find artibody failed', url
        return None
    rmsg = ''.join(rarr)
    return rmsg


# sinasoup 解析 获取目标路径
def parse_href(target, title):
    url_list = []
    if target is not None and len(target) > 0:
        for index in target:
            url_list.append(index.get("href"))
    else:
        print '页面解析器为None：', title
    return url_list
