# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 
# @Author  : ErichLee ErichLee@qq.com
# @File    : zimu_download.py
# @Comment : 
#            

import sys
from selenium import webdriver
from util.logger_util import *
import re
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def start():
    # 爬虫思路
    # step1 主页面，获取总 Page total，循环
    # step2 获取页面明细
    # step3 点击下一页，重复step2
    driver = webdriver.Chrome()
    with open('source/zimu2.txt', 'r') as ff:
        urls = ff.readlines()
        for url in urls:
            try:
                driver.get(url)
                driver.find_element_by_css_selector('a[class="btn-click"]').click()
            except Exception as e:
                infos("页面过期")
                continue

            time.sleep(2)

    time.sleep(10)
    driver.close()


start()
