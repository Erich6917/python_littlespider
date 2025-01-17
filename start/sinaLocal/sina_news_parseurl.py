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

import util.file_check_util as file_util
import util.date_check_util as dateUtil
import sinaSoup as bSoup

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
    filename = 'news_{}.txt'.format(time.strftime("%Y%m%d%H%M", time.localtime()))
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


def save_urls(urls):
    if urls:
        global gbl_file_urls
        gbl_file_urls.writelines('\n'.join(urls))
        gbl_file_urls.flush()


def parseurls_news_china():
    file_list = file_util.get_all_files_path_name('source/url')
    for file in file_list:
        file_name, file_path = file[0], file[1]
        print file_name, file_path
        with open(file_path, 'a+') as files:
            urls = files.readlines()
            parseurls_parse(urls)


def parseurls_parse(url_list):
    if not url_list:
        infos('没有需要解析的URL')
        return

    # url_list = list(set(url_list)) #去重暂时不需要

    # 结果返回字段

    infos('=============开始匹配=============== 初始请求条数', len(url_list), dateUtil.curr_date_format())
    counter_total = 0
    counter_exit = 0
    counter_error = 0

    # file_url_init()

    rt_msg_list = []

    for url in url_list:
        counter_total += 1
        r_msg = parseurls_msg(url)

        if counter_error > 1000:
            infos('ERROR.....错误次数太多，停止程序！')
            return
        if r_msg:
            counter_exit += 1

            infos('解析成功URL：[ {} ] URL > {}'.format(counter_total, url))
            rt_msg_list.append(r_msg)

            if counter_exit > 10000:
                # 批量保存
                # infos('批量保存中... {}'.format())
                # save_urls(rt_msg_list)
                # rt_msg_list = []

                # 生成新文件
                global gbl_path_output
                init_output_file(gbl_path_output)
                counter_exit = 0

            save_url(r_msg)

            counter_error = 0  # 连续失败次数重置为0

        else:
            counter_error += 1

    file_url_close()

    infos('=============匹配结束===============', '本次采集数量：')


def parseurls_msg(url):
    p_tech_old_normal = r'https?://news.sina.com.cn/s/.*'  # sina finace normal type
    p_tech_normal = r'https?://news.sina.com.cn/.*'  # sina finace normal type
    p_art_normal = r'https?://cul.news.sina.com.cn/.*'
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


#
# def parseurls_msg(url):
#     p_tech_old_normal = r'http://news.sina.com.cn/s/.*'  # sina finace normal type
#     p_tech_normal = r'http://news.sina.com.cn/.*'  # sina finace normal type
#     p_art_normal = r'http://cul.news.sina.com.cn/.*'
#     r_msg = ''
#     if re.match(p_tech_normal, url, re.M):
#         r_msg = bSoup.parse_news_normal(url)
#     elif re.match(p_art_normal, url, re.M):
#         r_msg = bSoup.parse_news_normal(url)
#     else:
#         infos('暂未匹配该路径', url)
#
#     return r_msg


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
    init_files()
    init_path()

    start_time = dateUtil.curr_date_format()
    infos('新浪爬虫START {0}'.format(start_time))

    parseurls_news_china()

    end_time = dateUtil.curr_date_format()
    infos('新浪爬虫END {0},COST > {1}'.format(end_time, (end_time - start_time)))


if __name__ == "__main__":
    start_news()
