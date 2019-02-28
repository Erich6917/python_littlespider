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

reload(sys)
sys.setdefaultencoding('utf-8')

url_java = 'http://www.runoob.com/java/java-tutorial.html'

hd = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Host': 'www.ximalaya.com'
}


def telnet(url):
    try:
        rt = requests.get(url)
        requests.encoding = 'utf-8'
        return BeautifulSoup(rt.content, 'lxml')
    except Exception as e:
        errors('访问失败！{}'.format(e))


def step_1_save_tel_content():
    url = 'http://www.runoob.com/'
    soup = telnet(url)
    url_list = soup.select('.codelist .item-top')
    for each in url_list:
        print each['href']


def step_2_save_tel_url():
    # url_list = [
    #     'http://www.runoob.com/java/java-tutorial.html',
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

    for each in file_url:
        detail = each.split('@@@')
        title, url = detail[0].decode('utf8'), detail[1]
        soup = telnet(url)
        msg_list = soup.select('div#content')
        try:
            with open(title, 'a') as file:
                for msg in msg_list:
                    # print each.text
                    file.write(msg.text + '\n')
        except Exception as e:
            print ("ERROR ", title)


def start():
    # step_1_save_tel_content()
    step_2_save_tel_url()
    # step_3_save_msg()


def get_telnet_url(url):
    soup = telnet(url)
    msg_list = soup.select('div#leftcolumn a')

    rt_telnet_url = []
    for each in msg_list:
        # print each['title'], each['href']
        try:
            tel_name = u'{}.txt'.format(each['title'])
        except Exception as e:
            tel_name = u'{}.txt'.format(random.randint(1, 1000))

        tel_url = 'http://www.runoob.com/{}'.format(each['href'])
        rt_telnet_url.append((tel_name, tel_url))
        # return [lambda msg_list: 'http://www.runoob.com'.format(each['href']) for each in msg_list]
    return rt_telnet_url


start()
