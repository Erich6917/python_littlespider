# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : finance.py
# @Commment: 新浪财经多线程爬虫
#

import re
import sys

import requests
import json

import dateCheckUtil as dateUtil
from bloom.sina.tools import sinaSoup as bSoup
from dbutil.DBNewsUtil import DBNews

reload(sys)
sys.setdefaultencoding('UTF-8')

import threading
import time
import types
import random
import finance as finance
import logging

con = threading.Condition()
flag = False
dbnews = DBNews()


def infos(*args):
    """
    :comment 同时print 和 打印日志
    :type args: object
    """

    for each in args:
        print each,
    print
    logging.info(args)


class UrlBox:
    def __init__(self):
        self.MAX_PULL = 20
        self.url_list = []  # 获取爬虫的URL集合

    def addUrls(self, curl):
        if isinstance(curl, str):
            if curl not in self.url_list:
                self.url_list.append(curl)
        elif isinstance(curl, list):
            self.url_list.extend(curl)

    def getUrls(self, gainSize=None):
        if gainSize:
            if gainSize > self.MAX_PULL or gainSize < 0:
                gainSize = self.MAX_PULL
        else:
            gainSize = self.MAX_PULL
        curls = self.url_list[:gainSize]  # 拿走当前库存中url，最多取走500个
        self.url_list = self.url_list[gainSize:]
        return curls

    def getBoxSize(self):
        return len(self.url_list)


def findSinaUrl():
    rtArr = []
    rtArr.append('http://sina1')
    rtArr.append('http://sina1')
    rtArr.append('http://sina1')
    rtArr.append('http://sina1')
    for ii in range(0, random.randint(1, 5)):
        rtArr.append('http://sina1')
    return rtArr


def findSouhuUrl():
    rtArr = []
    # rtArr.append('http://souhu1')
    return rtArr


class Producer(threading.Thread):
    def __init__(self, box, name, maxBox):
        super(Producer, self).__init__()
        self.box = box
        self.name = name
        self.maxBox = maxBox

    def run(self):
        global flag
        print self.name, "Producer " + self.name + " Start!\n"
        pstart = 1931
        steps = 20
        while pstart < 1981:#6500
            pend = pstart + steps
            print self.name, 'start:', dateUtil.currDateFormate()
            url_list = []
            # con.acquire()
            url_list.extend(finance._finance_geturl_china(pstart, pend))  # 国内财经

            if flag:
                # print self.name, "Producer wait\n"
                # con.wait()

                while self.box.getBoxSize() > self.maxBox:
                    print self.name, "Producer 暂无任务"
                    time.sleep(5)
                flag = False
            else:
                self.box.addUrls(url_list)
                print self.name, "Producer put: ", len(url_list)
                print self.name, "Producer BOX TOTAL : ", self.box.getBoxSize()
                if self.box.getBoxSize() > self.maxBox:
                    flag = True
                # con.notify()
                # con.release()
                # time.sleep(1)

            pstart += steps
            print self.name, 'end:', dateUtil.currDateFormate()

        print "The End of Producer !"


class Consumer(threading.Thread):
    def __init__(self, box, name, maxBox):
        super(Consumer, self).__init__()
        self.box = box
        self.name = name
        self.maxBox = maxBox

    def run(self):
        global flag
        time.sleep(5)
        print self.name, "Consumer " + self.name + " Start!\n"
        while True:

            url_list = self.box.getUrls()
            if not flag:
                # print self.name, "Consumer wait\n"
                # flag = True
                # con.acquire()
                # con.notify()
                # con.release()
                # time.sleep(5)
                while self.box.getBoxSize() < 1:
                    print self.name, "Consumer 暂无任务"
                    time.sleep(5)
                flag = True
            else:
                print self.name, "Consumer get: ", len(url_list)
                print self.name, "Consumer BOX TOTAL : ", self.box.getBoxSize()
                # if self.box.getBoxSize() < self.maxBox:
                if self.box.getBoxSize() < 1:
                    flag = False

                if url_list:
                    rdicts = finance.finance_parse_start(url_list)
                    scope = 'finance'
                    dbnews.save_sina_telnet_result(rdicts, scope)
                    print self.name, "save DB"

        print "The End of Consumer !"


if __name__ == '__main__':
    flag = False
    uBox = UrlBox()
    p = Producer(uBox, "SpiderMan", 50)
    c1 = Consumer(uBox, "SpiderParse1", 10)
    c2 = Consumer(uBox, "SpiderParse2", 10)
    p.start()
    c1.start()
    c2.start()
    # findSinaUrl()
