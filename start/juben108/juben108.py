# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 
# @Author  : ErichLee ErichLee@qq.com
# @File    : runoob_java.py
# @Comment : 
#            

import sys
import requests
import random
from bs4 import BeautifulSoup
from util.logger_util import *
from util.file_check_util import *
import re

reload(sys)
sys.setdefaultencoding('utf-8')

url_java = 'http://www.runoob.com/java/java-tutorial.html'

hd = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Host': 'www.juben108.com',
}


def telnet(url):
    try:
        rt = requests.get(url)  # , headers=hd
        # requests.encoding = 'utf-8'
        # print rt.text
        return BeautifulSoup(rt.content, 'html5')
    except Exception as e:
        errors('访问失败！{}'.format(e))


def step_1_save_tel_content():
    # url = 'http://www.juben108.com/telescript/'
    # url = 'http://www.juben108.com/Screenplay' # 电影
    url = 'http://www.juben108.com/wdy/'  # 微电影
    soup = telnet(url)
    url_list = soup.select('td.NAVZI b a')

    rt_list = []
    for each in url_list:
        try:
            tel_url = 'http://www.juben108.com/{}'.format(each['href'])
            rt_smg = '{}@@@{}'.format(tel_url, each.text)
            rt_list.append(rt_smg)
        except Exception as e:
            print (tel_url)
            continue



def step_find_content_detail():
    url = 'http://www.juben108.com/telescript_190_1_0/'
    max_page = find_max_page(url)


def step_2_save_tel_url():
    # url_list = [
    #     'http://www.juben108.com/telescript_190_1_0/',
    # ]
    file_content = open('content.txt', 'r')
    url_list = file_content.readlines()
    file_url = open('telnet_url.txt', 'a')
    for telnet_url in url_list:
        telnet_url = telnet_url.replace('\n', '')
        telnet_url_list = get_telnet_url(telnet_url)
        for each in telnet_url_list:
            title, url = each[0], each[1]
            rt_msg = u'{}@@@{}\n'.format(title, url)
            file_url.write(rt_msg)
    print (u'URL 获取完毕')


def step_3_save_msg():
    file_url = open('telnet_url.txt', 'a+')
    # file_url = ['http://www.juben108.com/telescript_88662_1/',
    #             # 'http://www.juben108.com/telescript_88650_1/'
    #             ]
    for each in file_url:
        detail = each.split('@@@')
        title, url = u'curr/{}'.format(detail[0].decode('utf8')), detail[1].replace('\n', '')
        soup = telnet(url)
        msg_list = soup.select('div#tab_contain #contain_4 p')

        try:
            print title
            with open(title, 'a+') as file:
                for msg in msg_list:
                    # print msg.text
                    file.write(msg.text + '\n')
        except Exception as e:
            print ("ERROR ", url, e)


def start():
    # step_1_save_tel_content()
    step_find_content_detail()
    # step_2_save_tel_url()
    # step_3_save_msg()

    # files = get_all_files(u'C:/Personal/workspace/mygit_py2/littlespider/start/juben108/curr')
    # for name in files:
    #     print name


def get_telnet_url(url):
    soup = telnet(url)
    msg_list = soup.select(
        'table.ylbroderfoot tbody tr td table tbody tr td table tbody tr td table tbody tr td font a')

    rt_telnet_url = []
    for each in msg_list:
        # print each['title'], each['href']
        # print each.text, each['href']
        try:
            tel_name = u'{}.txt'.format(each.text)
        except Exception as e:
            tel_name = u'{}.txt'.format(random.randint(1, 1000))
        #
        tel_url = 'http://www.juben108.com/{}'.format(each['href'])
        rt_telnet_url.append((tel_name, tel_url))
        # return [lambda msg_list: 'http://www.runoob.com'.format(each['href']) for each in msg_list]
    return rt_telnet_url


def find_max_page(url):
    soup = telnet(url)
    at = soup.select('#Page span')[0].text
    page_max = re.search(u'[0-9]+/([0-9])+页', at).group(1)
    return page_max


# find_max_page('http://www.juben108.com//wdy_365_1_0/')
start()
