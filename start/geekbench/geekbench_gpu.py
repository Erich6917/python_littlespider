# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 
# @Author  : ErichLee ErichLee@qq.com
# @File    : geekbench_start.py
# @Comment : 
#            

import sys
from bs4 import BeautifulSoup
import requests

# requests.adapters.DEFAULT_RETRIES = 5
reload(sys)
sys.setdefaultencoding('utf-8')

hd = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
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


def start_gpu():
    url_main = 'https://benchmarks.ul.com/compare/best-smartphones?amount=0&sortBy=PERFORMANCE&reverseOrder=true&osFilter=ANDROID,IOS&test=SLING_SHOT_ES_30&deviceFilter=PHONE&displaySize=3.0,15.0'
    soup = soup_request(url_main)
    print soup

    a_list = soup.select('table#productTable tbody tr td.pr1 a')
    print len(a_list)
    for a in a_list:
        print '{}@@@{}'.format(a['href'], a.text)
        # for index in range(1, page_total + 1):
        #     url = url_main.format(index)
        #     print 'parse ', url
        #     href_list = get_href_list(url)
        #     save_list(href_list)


def parse_detail_page(name, href):
    session = requests.session()
    session.keep_alive = False
    # session.proxies = {"https": "47.100.104.247:8080", "http": "36.248.10.47:8080", }
    # req = session.get(href)
    req = session.get(href, verify=False, headers=hd,timeout=10)
    soup = BeautifulSoup(req.text, 'lxml')
    rt_msg = []
    rt_msg.append(name.strip())
    # p1

    # find star
    stars = soup.select('div.starRating.clearfix span.icon-starConverted.full')
    rt_msg.append(' view:{')
    rt_msg.append(' {}@'.format(len(stars)))
    p1_dd_list = soup.select('div.padding.mt1 div div dt')
    p1_value = [value.text.strip() for value in p1_dd_list]
    rt_p1 = '@'.join(p1_value)
    rt_msg.append(rt_p1)
    # p2
    div_list = soup.select('.results .contentrow.clearfix div div')
    rt_msg.append('} Performance-value:{')
    for div in div_list:
        title = div.select_one('h3').text
        rt_msg.append(title + "[")
        dd_list = div.select('dt')
        # for dd in dd_list:
        #     print dd.text.strip()
        dd_value = [value.text.strip() for value in dd_list]
        rt_msg.append('@'.join(dd_value))
        rt_msg.append('] ')

    rt_msg.append('} Details:{')
    # p3

    p3_div_list = soup.select('div.device-details  div div div.data-container.mt05')
    for div in p3_div_list:
        # title = div.select_one('h3').text
        # rt_msg.append(title + "[")
        dd_list = div.select('dt')
        # for dd in dd_list:
        #     print dd.text.strip()
        dd_value = [value.text.replace('\n', '').replace('\r', '').replace(' ', '') for value in dd_list]
        rt_msg.append('@'.join(dd_value))
        rt_msg.append('] ')

    rt_msg.append('}')

    print ''.join(rt_msg)
    return ''.join(rt_msg) + '\n'


def start_parse_href():
    # rt_msg = []
    rt_ios = open('source/gpu_result.txt', 'a+')
    rt_error = open('source/gpu_error.txt', 'a+')

    with open('source/gpu_url.txt', 'a+') as file_ios:
        href_list = file_ios.readlines()
        # rt_list = list(set(href_list))
        for each in href_list:
            href, name = each.split('@@@')[0], each.split('@@@')[1]
            print 'start', name, href,

            try:
                msg = parse_detail_page(name, href)
                rt_ios.write(msg)
            except Exception as e:
                rt_error.write(each)
                rt_error.flush()
                print 'err', href, e
                # rt_msg.append(msg)

    rt_ios.close()
    rt_error.close()


if __name__ == '__main__':


    # start_parse_href()
    # start_gpu()
    parse_detail_page('plus', 'https://benchmarks.ul.com/hardware/phone/OnePlus+6T+review')
