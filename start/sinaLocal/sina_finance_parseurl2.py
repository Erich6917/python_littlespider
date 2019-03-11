# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : sina_news_parseurl.py
# @Comment : 新浪新闻页面整合处理
#

import os
import re
import socket
import sys
import time

import dateCheckUtil as dateUtil
import util.file_check_util  as file_check_util
from bloom.sina.tools import sinaSoup as bSoup

timeout = 20
socket.setdefaulttimeout(timeout)

reload(sys)
sys.setdefaultencoding('UTF-8')

gbl_path_source = 'source'
gbl_path_output = 'output'
gbl_file_urls = None
gbl_file_log = None


def infos(*args):
    if args:
        global gbl_file_log
        # str_lisSt = []
        # for each in args:
        #     str_list.append(str(each))
        # msg = ''.join(str_list)
        # print msg
        # gbl_file_log.write(msg + '\n')
        msg_arr = [str(each) for each in args]
        msg = ' '.join(msg_arr)
        print msg
        gbl_file_log.write('{}\n'.format(msg))


# infos('nihao', 'a', 'sbs')


def current_path():
    """
        获取当前文件路径
        兼容pycharm和cmd直接运行脚本路径
    """
    if getattr(sys, 'frozen', False):
        apply_path = os.path.dirname(sys.executable)
    elif __file__:
        apply_path = os.path.dirname(__file__)
    return apply_path


def init_path():
    source = os.path.join(current_path(), gbl_path_source)
    if not os.path.exists(source):
        infos('Create path {}'.format(source))
        os.mkdir(source)

    infos("Init Path...")


def init_files():
    global gbl_path_source, gbl_path_output, gbl_file_urls, gbl_file_log

    source = os.path.join(current_path(), gbl_path_source)
    if not os.path.exists(source):
        os.mkdir(source)

    gbl_path_output = os.path.join(source, 'output')
    if not os.path.exists(gbl_path_output):
        os.mkdir(gbl_path_output)

    init_output_file(gbl_path_output)

    if not gbl_file_log:
        curr_time = str(time.strftime("%Y%m%d%H%M", time.localtime()))
        logs_name = 'logs_{}.log'.format(str(curr_time))
        file_logs_name = os.path.join(source, logs_name)
        gbl_file_log = open(file_logs_name, 'a')
        infos("Create File {}".format(logs_name))


def init_output_file(path_source):
    global gbl_file_urls
    filename = 'finance_roll_{}.txt'.format(time.strftime("%Y%m%d%H%M", time.localtime()))
    file_output_name = os.path.join(path_source, filename)
    if gbl_file_urls:
        gbl_file_urls.close()
    gbl_file_urls = open(file_output_name, 'a')


def close_files():
    global gbl_file_urls, gbl_file_log
    if gbl_file_urls:
        gbl_file_urls.close()
    if gbl_file_log:
        gbl_file_log.close()
    infos("Close files...")


def save_url(url):
    if url:
        global gbl_file_urls
        # infos( url
        gbl_file_urls.write(url + '\n')


def parseurls_news_china(path_url):
    with open(path_url, 'a+') as files:
        urls = files.readlines()
        parseurls_parse(urls)


def parseurls_parse(url_list):
    if not url_list:
        infos('没有需要解析的URL')
        return

    # url_list = list(set(url_list)) #去重暂时不需要

    # 结果返回字段

    infos('=============开始匹配=============== 初始请求条数', len(url_list), dateUtil.currDateFormate())
    counter_total = 0
    counter_exit = 0
    counter_error = 0

    # file_url_init()

    for url in url_list:
        counter_total += 1
        r_msg = parseurls_msg(url)

        if counter_error > 1000:
            infos('ERROR.....错误次数太多，停止程序！')
            return
        if r_msg:
            counter_exit += 1

            if counter_exit > 10000:
                global gbl_path_output
                init_output_file(gbl_path_output)
                counter_exit = 0

            infos('解析成功URL：[ {} ] URL > {}'.format(counter_total, url))
            save_url(r_msg)

            counter_error = 0  # 连续失败次数重置为0

        else:
            counter_error += 1

    file_url_close()

    infos('=============匹配结束===============', '本次采集数量：')


def parseurls_msg(url):
    p_tech_old_normal = r'http://news.sina.com.cn/s/.*'  # sina finace normal type
    p_tech_normal = r'http://news.sina.com.cn/.*'  # sina finace normal type
    p_art_normal = r'http://cul.news.sina.com.cn/.*'
    p_finance = r'https?://finance.sina.com.cn/.*'  # sina finace normal type
    p_blog = r'https?://blog.sina.com.cn/s/.*'  # sina blog
    r_msg = ''
    if re.match(p_tech_normal, url, re.M):
        r_msg = bSoup.parse_news_normal(url)
    elif re.match(p_art_normal, url, re.M):
        r_msg = bSoup.parse_news_normal(url)
    elif re.match(p_finance, url, re.M):
        r_msg = bSoup.parse_tech_normal(url)
    else:
        infos('暂未匹配该路径', url)

    return r_msg


# def file_url_init():
#     filename = 'news_{}.txt'.format(time.strftime("%Y%m%d%H%M", time.localtime()))
#     global gbl_file_urls
#     gbl_file_urls = open(filename, 'a')
#
#
# def file_url_new():
#     global gbl_file_urls
#     if gbl_file_urls:
#         gbl_file_urls.close()
#     filename = 'news_{}.txt'.format(time.strftime("%Y%m%d%H%M", time.localtime()))
#     gbl_file_urls = open(filename, 'a')


def file_url_close():
    global gbl_file_urls
    if gbl_file_urls:
        gbl_file_urls.close()


def start_news():
    path_url = 'source/url/sina_news_2019012214000009.txt'
    init_files()
    init_path()

    start_time = dateUtil.currDateFormate()
    infos('新浪爬虫START {0}'.format(start_time))

    parseurls_news_china(path_url)

    end_time = dateUtil.currDateFormate()
    infos('新浪爬虫END {0},COST > {1}'.format(end_time, (end_time - start_time)))


def start_new_task(file_name, file_path):
    init_files()
    init_path()

    start_time = dateUtil.currDateFormate()
    infos('解析文本 [{0}] START {1}'.format(file_name, start_time))

    parseurls_news_china(file_path)

    end_time = dateUtil.currDateFormate()
    infos('解析文本 [{0}] END {1},COST > {2}'.format(file_name, end_time, (end_time - start_time)))


def start_finance():
    file_list = file_check_util.get_all_files_path_name('source/url_finance2')
    for target in file_list:
        file_name, file_path = target[0], target[1]
        start_new_task(file_name, file_path)

def re_read_file(file_name, wt_file_name):
    try:
        results = open(file_name, 'rU')  # 打开文件
        write_file = open(wt_file_name, 'w+')
        new_data = ''
        for count, line in enumerate(results):
            if line in write_file:
                print line
                continue
            else:
                # new_data += line + '\n'
                write_file.write(line)
        # write_file.write(new_data + '\n')
    except Exception, e:
        print(e)
    finally:
        results.close()
        write_file.close()
if __name__ == "__main__":
    # start_news()

    start_finance()

    # url = 'https://finance.sina.com.cn/money/insurance/bxyx/2018-09-29/doc-ihkmwytp8639714.shtml'
    # url = 'https://finance.sina.com.cn/china/gncj/2018-10-04/doc-ihkmwytp8549195.shtml'
    # url = 'https://finance.sina.com.cn/blockchain/roll/2018-09-29/doc-ifxeuwwr9427469.shtml'
    # url = 'https://finance.sina.com.cn/stock/hyyj/2018-09-29/doc-ifxeuwwr9426730.shtml'
    # print parseurls_msg(url)