# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 
# @Author  : ErichLee ErichLee@qq.com
# @File    : crops_spider.py
# @Comment : 中国作物种质信息网 http://www.cgris.net/query/croplist.php
#            


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

    url = 'http://www.cgris.net/query/do.php#其它作物,橡胶'
    browser_query(driver, url)

    page_total = browser_page_total(driver)
    if not page_total:
        return

    with open('crops_messages.txt', 'w+') as file_crops:
        for page_index in range(4008, page_total + 1):
            page_msg = get_page_msg(driver)  # 获取页面信息，并且保存
            file_crops.write(page_msg)

            browser_next_page(driver)  # 点击下一页


def get_page_msg(driver):
    css_list = browser_target_css()
    rt_msg = ''
    rt_key = ''
    rt_value = ''
    for tar_ele in css_list:
        try:
            rt_key = driver.find_element_by_css_selector(tar_ele[0]).text
            rt_value = driver.find_element_by_css_selector(tar_ele[1]).text
        except Exception, e:
            errors("errors > {}".format(e))
        rt_msg += '[{0:<5}:{1:<20}]@'.format(rt_key, rt_value)
    return rt_msg + '\n'


def browser_target_css():
    # 页面分析 18行 每行6列，可分为三组
    css_list = []
    css_base = '#r2 > table> tbody> tr> td> div> table> tbody> tr:nth-child({}) > td:nth-child({})'
    for row in range(1, 19):
        for index in range(1, 7, 2):
            tar_key = css_base.format(row, index)
            tar_value = css_base.format(row, index + 1)
            css_list.append((tar_key, tar_value))
    return css_list


def browser_page_total(driver):
    driver.implicitly_wait(2)
    total_msg = driver.find_element_by_css_selector("div[id='r1']")
    infos('捕获文本TOTAL信息 > {}'.format(total_msg.text))
    rt = re.search(u'共找到([0-9]+)个结果', total_msg.text)
    if rt:
        page_total = rt.group(1)
        infos('当前种类共计结果条数[{}]'.format(page_total))
        return int(page_total)
    errors('当前种类未找到结果总数，停止当前种类查找！')


def browser_query(driver, url):
    driver.get(url)
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('div[onclick="query()"]').click()
    driver.implicitly_wait(2)
    time.sleep(2)


def browser_next_page(driver):
    driver.implicitly_wait(3)
    driver.find_element_by_css_selector('a[id="nexthehe"]').click()


start()
