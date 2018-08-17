# -*- coding: utf-8 -*-
# @Time    : 2018/8/7 
# @Author  : ErichLee ErichLee@qq.com
# @File    : jd_spider.py
# @Comment : 
#            

from selenium import webdriver
from util.logger_util import *
import sys
import time
import win32api
import win32con

reload(sys)
sys.setdefaultencoding('utf-8')
contents = [
    'https://search.jd.com/Search?keyword=%E4%BC%91%E9%97%B2%E9%A3%9F%E5%93%81&enc=utf-8&wq=%E4%BC%91%E9%97%B2%E9%A3%9F%E5%93%81&pvid=s742apui.nhltvu',
    # 'https://search.jd.com/Search?keyword=%E7%89%9B%E5%A5%B6&enc=utf-8&wq=%E7%89%9B%E5%A5%B6&pvid=5wh5apui.nhltvu',
    # 'https://search.jd.com/Search?keyword=%E9%A5%AE%E6%96%99&enc=utf-8&wq=%E9%A5%AE%E6%96%99&pvid=ohs0apui.nhltvu',
]


def start():
    driver = webdriver.Chrome()
    for url in contents:
        driver.get(url)
        time.sleep(2)
        goods_list = get_all_goods(driver)
        if goods_list:
            save_goods(goods_list)
            # driver.close()


def save_goods(good_list):
    with open('goods.txt', 'a') as goods:
        for good in good_list:
            rt_good = '{}\n'.format(good)
            goods.write(rt_good)


def get_all_goods(driver):
    xpath = '//div[@id="J_goodsList"]/ul/li/div/div[4]/a/em'
    move_page_end(driver)
    time.sleep(5)

    tags = driver.find_elements_by_xpath(xpath)
    # infos('AFTER LENG>{}'.format(len(tags)))

    # for tag in tags:
    #     infos(tag.text)
    goods_list = [tag.text for tag in tags]
    return goods_list


def move_page_end(driver):
    # 鼠标移动到页面底部
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -12000)


start()
