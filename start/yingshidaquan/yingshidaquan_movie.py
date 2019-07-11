# -*- coding: utf-8 -*-
# @Time    : 2019/1/2 
# @Author  : ErichLee ErichLee@qq.com
# @File    : yingshidaquan_movie.py
# @Comment : 
#            

import sys
import time
import re
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

hd = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Host': 'www.yingshidaquan.com'
}


def soup_request(url):
    try:
        req = requests.get(url)
        req.encoding = 'utf-8'
        return BeautifulSoup(req.text, 'html5lib')
    except Exception, e:
        print (e)
        return ''


def get_movie_detail(url):
    soup = soup_request(url)
    a_list = soup.select('.movielist ul li a.p')
    detail_list = []
    for a_label in a_list:
        href, title = 'http://www.yingshidaquan.com/{}'.format(a_label['href']), (a_label['title'])
        title = str(title).replace(u'/在线播放', '').replace(' ', '')
        # print href, title
        detail_list.append((href, title))
        # print  (a_label['title'])
    return detail_list


def tv_download(detail_list):
    file_url = open('href.txt', 'a+')
    for detail in detail_list:
        href, title = detail[0], detail[1]
        rt = '{}@@@{}\n'.format(href, title)
        # print 'start ', href[0]
        try:
            file_url.write(rt)
        # soup = soup_request(href)
        #     # div.endpage div div
        #     input_list = soup.select('ul.downurl')
        #     time.sleep(2)
        #     for target in input_list:
        #         # print target['name']
        #         print target
        except Exception as e:
            print ('ERROR tv_download', href)


def tv_mainland_start():
    telnet_url = 'http://www.yingshidaquan.com/vod-show-id-15-year--area--order-filmtime-p-{}.html'
    page_max = 310
    for page in range(1, page_max):
        print 'download... page ', page
        url = telnet_url.format(page)
        detail_list = get_movie_detail(url)
        tv_download(detail_list)


def tv_parse_href(href_list):
    regex = 'decodeURI\(([^)]+)\)'
    for href in href_list:
        print href
        soup = soup_request(href)
        # print soup.text

        result = re.search(regex, soup.text)
        if result:
            # print result.group(1)  #测试输出
            return result.group(1)
        else:
            return None


def tv_parse_json(href):
    regex = 'decodeURI\(([^)]+)\)'
    soup = soup_request(href)
    # print soup.text

    result = re.search(regex, soup.text)
    if result:
        # print result.group(1)  #测试输出
        return result.group(1)
    else:
        return ''


def parse_page_detail():
    # url = 'http://www.yingshidaquan.com//html/DQ315206.html'
    # url = 'http://www.yingshidaquan.com//html/DQ315203.html'
    # url = 'http://www.yingshidaquan.com//html/DQ314777.html'
    file_rt = open('href_result.txt','a+')
    with open('href.txt', 'a+') as file_movie:
        url_list = file_movie.readlines()
        for url_msg in url_list:
            url = url_msg.split('@@@')[0]
            type_msg = tv_parse_json(url)
            type_msg = type_msg.replace("\"", "")
            rt_list = type_msg.split('###')
            rt_msg =[]
            for each in rt_list:
                # print re.sub("[^$]+\$", "", each)
                rt_href = re.sub("[^$]+\$", "", each)
                rt_msg.append(rt_href)
            print 'write msg ...'
            file_rt.write("\n".join(rt_msg))
            file_rt.write("\n")
            file_rt.flush()


def start():
    tv_mainland_start()


parse_page_detail()
