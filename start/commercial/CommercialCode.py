# -*- coding: utf-8 -*-
# @Time    : 2018/9/12 
# @Author  : ErichLee ErichLee@qq.com
# @File    : CommercialCode.py
# @Comment : 
#            

import sys
import time

from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')


def start():
    driver = webdriver.Chrome()

    url = 'http://chinesecommercialcode.net/search/index/zh'
    driver.get(url)
    time.sleep(3)

    for index in range(6089, 9999):
        key_select = '{0:0>4}'.format(index)
        driver.find_element_by_xpath('//input[@name="searchbox"]').send_keys(key_select)
        while True:
            try:
                driver.find_element_by_xpath('//input[@name="submit"]').click()
                break
            except Exception as e:
                time.sleep(3)
        target = driver.find_elements_by_xpath('//div[@class="item"]/p')
        for each in target:
            print each.text,
        print

start()
