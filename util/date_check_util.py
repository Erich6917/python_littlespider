# -*- coding: utf-8 -*-
# @Time    : 2018/6/4
# @Author  : ErichLee ErichLee@qq.com
# @File    : date_check_util.py
# @Comment : 日期类检查工具
#
import datetime
import time


def __curr_time():
    print time.time()
    print time.localtime((time.time()))
    print time.localtime()

    print time.strftime("%Y-%m-%d %H:%M:%S %Y", time.localtime())

    print datetime.datetime.now()


def curr_date_str():
    return time.strftime("%Y-%m-%d", time.localtime())


def curr_date_str2():
    return time.strftime("%Y%m%d", time.localtime())


def curr_data_ymdhm():
    return str(time.strftime("%Y%m%d%H%M", time.localtime()))


def curr_date_format():
    now_time = datetime.datetime.now()
    return now_time
