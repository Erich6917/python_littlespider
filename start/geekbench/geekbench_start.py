# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 
# @Author  : ErichLee ErichLee@qq.com
# @File    : geekbench_start.py
# @Comment : 
#            

import sys
from bs4 import BeautifulSoup
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

hd = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Host': 'browser.geekbench.com'
}


def soup_request(urls, coding='utf-8'):
    res = requests.get(urls)
    res.encoding = coding

    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(res.text, 'html5lib')
    return rsoup


def get_href_list(url):
    soup = soup_request(url)
    tr_list = soup.select('div#wrap .table-responsive table tbody tr')
    href_list = []
    for tr in tr_list:
        name = tr.select_one('td.model a').text
        href = tr.select_one('td.model a')['href']
        Platform = tr.select_one('td.platform').text
        href = 'https://browser.geekbench.com/' + href
        # rt_msg = '{}@@@{}@@@{}'.format(name, href, Platform)
        # print name, href, Platform
        href_list.append((name, href, Platform))
    return href_list


def save_list(href_list):
    file_ios = open('source/ios_url.txt', 'a+')
    file_android = open('source/android_url.txt', 'a+')
    file_other = open('source/other_url.txt', 'a+')
    for each in href_list:
        name, href, Platform = each[0], each[1], each[2]
        rt_msg = '{}@@@{}\n'.format(name, href)
        if 'iOS 64-bit' in Platform:
            file_ios.write(rt_msg)
        elif 'Android 64-bit' in Platform:
            file_android.write(rt_msg)
        else:
            file_other.write(rt_msg)


def start_cpu():
    page_total = 1000
    url_main = 'https://browser.geekbench.com/v4/cpu?page={}'
    for index in range(1, page_total + 1):
        url = url_main.format(index)
        print 'parse ', url
        href_list = get_href_list(url)
        save_list(href_list)


def parse_detail_page(name, href):
    # soup = soup_request(href)
    # tbody_list = soup.select_one('.table-responsive table')
    # for tbody in tbody_list:
    #     print tbody
    # print tbody_list[0]
    req = requests.get(href, headers=hd)
    soup = BeautifulSoup(req.text, 'lxml')
    table_list = soup.select('table.table.geekbench2-show.section-performance')

    rt_msg = []
    rt_msg.append(name)

    rt_msg.append('[Single-Core Performance]')

    single_list = table_list[0].select('tr th')
    for each in single_list:
        msg = each.text.strip()
        if msg:
            rt_msg.append(each.text)

    #
    rt_msg.append('[Multi-Core Performance]')

    single_list = table_list[1].select('tr th')
    for each in single_list:
        msg = each.text.strip()
        if msg:
            rt_msg.append(each.text)
    return '@'.join(rt_msg) + '\n'


    # single_p2_list = table_list[3].select('tbody tr')
    # for each in single_p2_list:
    #     print each['class'], each.text


    # single_list = table_list[4].select('thead tr th')
    # for each in single_list:
    #     print each['class'].text, each.text
    # print table_list[4]

    # print soup


def start_parse_href():
    rt_msg = []
    with open('source/android_url.txt', 'a+') as file_ios:
        href_list = file_ios.readlines()
        print len(href_list)
        rt_list = list(set(href_list))
        print len(rt_list)
        for each in rt_list:
            name, href = each.split('@@@')[0], each.split('@@@')[1]
            print 'start', name, href
            msg = parse_detail_page(name, href)
            rt_msg.append(msg)
    with open('source/android_result.txt', 'a+') as rt_ios:
        rt_ios.writelines(rt_msg)


if __name__ == '__main__':
    start_parse_href()
    # start_cpu()
    # parse_detail_page('https://browser.geekbench.com//v4/cpu/12142628')
