# -*- coding: utf-8 -*-
# @Time    : 2019/7/2
# @Author  : ErichLee ErichLee@qq.com
# @File    : kongfuzi.py
# @Comment :
#
import time
import sys
import re
import os
import requests
import util.logger_util as logger
import json
import util.file_check_util as file_util
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
'''
网站首页 http://bq.kongfz.com/

'''
hd = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'Host': 'item.kongfz.com',
}
hd_host = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'Host': 'bq.kongfz.com',
}


def telnet(url):
    try:
        rt = requests.get(url, headers=hd)  # , headers=hd
        # requests.encoding = 'utf-8'
        # print rt.text
        return BeautifulSoup(rt.text, 'html5lib')
        # return rt.text
    except Exception as e:
        logger.errors('访问失败！{}'.format(e))


def telnet_host(url):
    try:
        rt = requests.get(url, headers=hd_host)  # , headers=hd
        # requests.encoding = 'utf-8'
        # print rt.text
        return BeautifulSoup(rt.text, 'html5lib')
        # return rt.text
    except Exception as e:
        logger.errors('访问失败！{}'.format(e))


def get_context_detail(href):
    # href = 'http://item.kongfz.com/Cxiaoshuo/tag_k4e2dk56fdk53e4k5178k5c0fk8bf4w2/'
    print 'telnet', href
    time.sleep(1)

    soup = telnet(href)

    item_list = soup.select('div#listBox .item-info')

    rt_list = []
    for item in item_list:
        title = item.select_one('.title a').text
        href_target = item.select_one('.title a')['href']

        span_list = item.select('.zl-isbn-info span')
        msg_list = [msg.text for msg in span_list]
        details = ''.join(msg_list)
        msg = '{}\t{}\t{}'.format(title, details, href_target)
        rt_list.append(msg)

    return rt_list


    # print msg
    # msg_json = json.loads(msg)
    # filterList = msg_json['data']['filterList']
    # for each in filterList:
    #     print each.get('title'),each.get('name')


# get_context_detail()

def get_main_page_size(href):
    soup = telnet(href)
    return int(soup.select_one('div#pagerBox')['countpage'])


# 种类 - 分类  class  -classify
def main_root_classify(kind, classify, href):
    # kind, classify, href = u'小说', u'中国古典小说', 'http://item.kongfz.com/Cxiaoshuo/tag_k4e2dk56fdk53e4k5178k5c0fk8bf4/'

    page_max = get_main_page_size(href)

    href_list = []
    href_list.append(href)

    for index in range(2, page_max + 1):
        href_new = re.sub('/$', 'w{}/'.format(index), href)
        href_list.append(href_new)

    soure_path = 'source'
    file_name = classify + '.txt'
    target_path = os.path.join(soure_path, kind)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    file_path = os.path.join(target_path, file_name)
    print file_path
    with open(file_path, 'a+') as file_garget:
        file_garget.writelines('\n'.join(href_list))
        # 遍历所有页面 保存内容


def main_content_list():
    href = 'http://bq.kongfz.com/'
    soup = telnet_host(href)
    sign_list = soup.select('div.wrap-outer .module .one-sign')
    for a in sign_list:
        if a.select_one('a'):
            print a.select_one('a').text
            next_ele = a.findNext('div')

            a_list = next_ele.select('a')

            for a_detail in a_list:
                href = a_detail['href']
                title = a_detail.select_one('div').text
                print title, href

                # title, href = next_ele.select_one('div').text, next_ele.select_one('a')['href']
                # print title,href
                # a_list = soup.select('div.wrap-outer .module .sign-search a')
                # for a in a_list:
                #     print a['href'],a.select_one('div').text


def get_context_msg():
    lines = open('context.txt', 'a+').readlines()
    context = ''
    for line in lines:
        line_arr = line.strip().split('\t')
        if len(line_arr) == 1:
            context = line_arr[0]
            continue
        print '{}\t{}\t{}'.format(context, line_arr[0], line_arr[1])


# main_content_list()


def start_step1():
    lines = open('main.txt', 'a+').readlines()
    for line in lines:
        line_arr = line.strip().split('\t')
        kind, classify, href = line_arr[0], line_arr[1], line_arr[2]
        main_root_classify(kind.decode('utf-8'), classify.decode('utf-8'), href)


def start_step2():  #
    soure_path = u'source'
    file_list = file_util.get_all_files_path_name_endswith(soure_path, '.txt')
    for name, path, root in file_list:
        print name, path, root

        output_root = root.replace(u'source', u'output')
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        file_output = open(os.path.join(output_root, name), 'a+')

        lines = open(path, 'a+').readlines()
        for href in lines:
            msg_list = get_context_detail(href.strip())
            file_output.writelines('\n'.join(msg_list))

        time.sleep(10)


def start_step3_clean():  #
    soure_path = u'output'
    file_list = file_util.get_all_files_path_name_endswith(soure_path, '.txt')
    for name, path, root in file_list:
        print name, path, root

        output_root = root.replace(u'output', u'job')
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        file_output = open(os.path.join(output_root, name), 'a+')

        lines = open(path, 'r').readlines()
        for line in lines:
            line_arr = line.strip().split('\t')
            if len(line_arr) >= 2:
                title, author = line_arr[0], line_arr[1]
                author_arr = author.split('/')
                if len(author_arr) >= 2:
                    out_author, out_publishing = author_arr[0], author_arr[1]
                    msg = '{} @@@ {} @@@ {}\n'.format(title, out_author, out_publishing)
                    file_output.write(msg)

        if file_output:
            file_output.close()


def def_step_summary():
    source = u'job'
    kinds = file_util.get_all_dir_names(source)
    total = 0
    for kind in kinds:
        path_kind = os.path.join(source, kind)
        print kind
        total_classify = 0
        classifies = file_util.get_all_filename(path_kind)
        for classify in classifies:
            counter = len(open(os.path.join(path_kind, classify)).readlines())
            total += counter
            total_classify += counter
            print '--', classify, '--', counter
        print kind, total_classify
    print 'TOTAL', total


def_step_summary()
