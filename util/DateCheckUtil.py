# coding=utf-8
'''
Created on 2017年9月4日

@author: Administrator
'''

import datetime
import time


# (1)字符串转datetime：
# def strToDate(dateStr):
#     string = '2014-01-08 11:59:58'
#     time1 = datetime.datetime.strptime(string,'%Y-%m-%d %H:%M:%S')
#     print time1

# (2)datetime转字符串：
# def DateToStr():
#     time1_str = datetime.datetime.strftime(time1,'%Y-%m-%d %H:%M:%S')
#     print time1_str

#
# now_time = datetime.datetime.now()
# timeStr = datetime.datetime.strftime(now_time,'%Y-%m-%d')
# print timeStr

def currDateFormateA():
    now_time = datetime.datetime.now()
    timeStr = datetime.datetime.strftime(now_time, '%Y-%m-%d')
    timeDate = datetime.datetime.strptime(timeStr, '%Y-%m-%d')
    return timeDate


def currDateFormate():
    now_time = datetime.datetime.now()
    return now_time


def currY_M_D():
    return time.strftime("%Y-%m-%d", time.localtime())


def currYMD():
    return time.strftime("%Y%m%d", time.localtime())
