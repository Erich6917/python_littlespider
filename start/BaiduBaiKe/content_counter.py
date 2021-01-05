# -*- coding: utf-8 -*-
# @Time    : 2019/8/9
# @Author  : ErichLee ErichLee@qq.com
# @File    : content_counter.py
# @Comment :
#

import os
import re
import socket
import sys
import time
import urllib2

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 5
socket.setdefaulttimeout(timeout)

hd_type = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'baike.baidu.com',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'Referer': 'https://baike.baidu.com/item/%E6%B7%B1%E5%9C%B3%E8%AF%81%E5%88%B8%E4%BA%A4%E6%98%93%E6%89%80?fromtitle=%E6%B7%B1%E4%BA%A4%E6%89%80&fromid=11175110',

    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': 'BAIDUID=B1D1505BF9A5B40B1A281FF3DE174549:FG=1; PSTM=1554198827; BIDUPSID=67C9759455A6754A2A945E7CF2A553D6; MCITY=-%3A; BDUSS=1LanNyeU1uc1RyUmY0TTYxRkhVflZpdlB4Z3B0fng0S0VIaERtQUhEbnBuWFJkSVFBQUFBJCQAAAAAAAAAAAEAAACsGusMy8W7-rT9t6LFtgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOkQTV3pEE1dQU; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E6%95%85%E6%84%8F%E4%BC%A4%E5%AE%B3%E7%BD%AA%22%2C%22%E5%BE%88%E5%B0%8F%22%2C%22%E7%82%89%E7%9F%B3%E4%BC%A0%E8%AF%B4%22%2C%22%E7%BB%8F%E6%B5%8E%22%2C%22%E6%95%85%E6%84%8F%E4%BC%A4%E5%AE%B3%22%2C%22%E6%B7%B1%E4%BA%A4%E6%89%80%22%2C%22dc%E7%94%B5%E5%BD%B1%22%2C%22%E7%99%BD%E8%8C%B6%22%2C%22%E5%8F%98%E5%BD%A2%E9%87%91%E5%88%9A4%22%2C%22%E5%BE%AE%E5%8D%9A%22%5D%7D; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1424_21115_29522_29521_29098_29567_29220_29071_22158; delPer=0; PSINO=5; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; pgv_pvi=8433565696; pgv_si=s312635392; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1565590587,1565860220,1566208438,1566280701; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1566285824'

}


def telnet(url):
    response = urllib2.urlopen(url)
    if response.getcode() != 200:
        return None
    return response.read()


def telnet_code(url):
    html_cont = telnet(url)

    matcher = re.search('lemmaId=([0-9]+)\'', html_cont)
    if matcher:
        code = matcher.group(1)
    else:
        return None, None

    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    span_list = soup.select('span.taglist')

    msg_list = [span.text.strip() for span in span_list]

    return code, ' '.join(msg_list)


def telnet_like(url):
    html_cont = telnet(url)

    matcher = re.search('likeCount\":\"([0-9]+)\"', html_cont)
    if matcher:
        return matcher.group(1)


def start(key, times):
    url = u'https://baike.baidu.com/item/{}'.format(key)

    code, tag = telnet_code(url)
    if not code:
        # print u'未找到对应的词条', key
        return

    url_like = u'https://baike.baidu.com/api/wikiui/sharecounter?lemmaId={}&method=get'.format(code)
    like = telnet_like(url_like)

    msg = '{}\t{}\t{}\t{}\n'.format(key, times, like, tag)
    return msg


def curr_ymd_hms():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def curr_datetime():
    return time.strftime("%H:%M:%S", time.localtime())


def get_all_files_path_name(path_source='.'):
    file_list = []
    for root, dirs, files in os.walk(path_source):
        for filename in files:
            file_msg = filename, os.path.join(root, filename), root
            file_list.append(file_msg)
    return file_list


def init():
    path_source = u'source/txt'
    file_list = get_all_files_path_name(path_source)
    counter = 0
    # time.
    msg_succ = []
    msg_fail = []
    for file_name, file_path, root in file_list:
        print file_name, file_path, root
        lines = open(file_path, 'r').readlines()
        total = len(lines)
        print file_name, 'total', total

        file_out_succ = open('source/out/succ{}.txt'.format(curr_ymd_hms()), 'w')
        file_out_fail = open('source/out/fail{}.txt'.format(curr_ymd_hms()), 'w')

        for line in lines:
            counter += 1

            key = line.strip().split(' ')
            if len(key) == 5:
                try:
                    key, times = key[0].strip(), key[4].strip()
                    msg = start(key, times)
                    if msg:
                        msg_succ.append(msg)
                        print 'ok'
                    else:
                        msg_fail.append(line)
                except Exception as e:
                    msg_fail.append(line)
                    print 'ERROR', e
            else:
                msg_fail.append(msg)

            if counter % 5 == 0:
                print '({}/{})/{}'.format(counter, total, curr_datetime())
                file_out_succ.writelines(''.join(msg_succ))
                file_out_succ.flush()
                msg_succ = []
                file_out_fail.writelines(''.join(msg_fail))
                file_out_fail.flush()
                msg_fail = []
    if msg_succ:
        file_out_succ.writelines(''.join(msg_succ))
        file_out_succ.flush()
    if msg_fail:
        file_out_fail.writelines(''.join(msg_fail))
        file_out_fail.flush()


init()
