# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_download.py
# @Comment : 
#            

import sys
import re
import sys

import os
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from selenium.webdriver.chrome.options import Options

# import util.file_check_util as file_util
# from util.logger_util import *


def get_all_files_path_name(path_source='.'):
    file_list = []
    for root, dirs, files in os.walk(path_source):
        for filename in files:
            file_msg = filename, os.path.join(root, filename), root
            file_list.append(file_msg)
    return file_list


def get_Chrome_options():
    chromeOpitons = Options()
    prefs = {
        "profile.managed_default_content_settings.images": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,

    }

    chromeOpitons.add_experimental_option('prefs', prefs)
    return chromeOpitons


class mainAll(object):
    __path_source = 'output'

    def __init__(self):

        self.file_url = None  # URL读取文件
        self.file_error = None  # 日志错误记录
        self.file_log = None  # 日志常规记录

        try:

            self.scrapy_start()

        except Exception as e:
            print('异常退出！{}'.format(e))
        finally:
            self.the_end()

        print("ok,the work is done!")

    def write_error_url(self, err_msg):
        self.file_error.write(err_msg)
        self.file_error.flush()

    def scrapy_start(self):
        source_info = 'source/infos'
        file_list = get_all_files_path_name(source_info)

        for file_name, file_path, file_root in file_list:
            with open(file_path) as file_href:
                lines = file_href.readlines()

                list_href = [line.replace('\n', '') for line in lines]

                # self.init()  # 初始化日志

                # url_list = self.get_source_url()

            output_root = file_root.replace('/infos', '/jumps')
            if not os.path.exists(output_root):
                os.makedirs(output_root)
            output_path = os.path.join(output_root, 'source_init_jump.txt')
            print file_name, file_path, len(list_href), output_path
            file_select = open(output_path, 'a+')
            file_err_log = open(os.path.join(output_root, 'error.log'), 'a+')

            for url_info in list_href:
                try:
                    # url = 'http://tingshen.court.gov.cn/live/5202044'
                    catalog_id = url_info.split('\t')[0]
                    url = 'http://tingshen.court.gov.cn/live/{}'.format(catalog_id)
                    print 'telnet', url
                    driver = self.login(url)

                    msg = '{}\t{}\n'
                    if not driver:
                        print('登录失败!', url)
                        file_err_log.write(msg.format('登录失败', catalog_id))
                        file_err_log.flush()
                        continue
                    url_jump = self.search_jump_url(driver)

                    if not url_jump:
                        print '获取是失败', url
                        file_err_log.write(msg.format('登录失败', catalog_id))
                        file_err_log.flush()
                    else:
                        file_select.write(msg.format(url_jump, catalog_id))
                        file_select.flush()

                except Exception as e:
                    print url, e
                    # err_msg = '{}\n'.format(url)
                    file_err_log.write(msg.format(e, catalog_id))
                    file_err_log.flush()
                    continue
                finally:
                    if driver:
                        driver.close()


                        # print url_jump
                        # driver.get(url_jump)
                        # time.sleep(1)
                        #
                        # source_target = self.search_real_url(driver)

                        # if source_target:
                        #     print 'SUCCESS ! ! !', source_target
                        #     rt_msg = '{}\t{}\n'.format(url, source_target)
                        #     self.file_url.write(rt_msg)
                        #     self.file_url.flush()
                        # else:
                        #     err_msg = '{}\n'.format(url)
                        #     self.file_error.write(err_msg)
                        #     self.flush()

    def search_real_url(self, driver):

        download_href = driver.find_element_by_xpath(''
                                                     '//video[@id="index_player_html5_api"]'
                                                     '/source'
                                                     '')
        if download_href:
            return download_href.get_attribute('src')

    def search_jump_url(self, driver):
        # download_href = driver.find_element_by_xpath('//div[@id="container"]').text

        # http://player.videoincloud.com/vod/3248777?src=gkw&cc=1
        download_href = driver.find_element_by_xpath(''
                                                     '//div[@class="live-video-content"]'
                                                     '/div'
                                                     '/iframe[@id="player"]'
                                                     ''
                                                     )
        # download_href = driver.find_element_by_xpath('//video[@id="index_player_html5_api"]/source')
        if download_href:
            return download_href.get_attribute('src')

    def login(self, url):
        try:
            driver = webdriver.Chrome(chrome_options=get_Chrome_options())
            # driver = webdriver.Chrome()
            driver.get(url)
            driver.set_page_load_timeout(20)
            element = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id('player'))
            # driver.implicitly_wait(2)
            # time.sleep(0.5)
            return driver
        except Exception as e:
            print e

    def get_source_url(self):
        with open('source/source_init_select.txt', 'r+') as file_url:
            lines = file_url.readlines()

            rt_list = [line.replace('\n', '') for line in lines]
        return rt_list

    def init(self):
        self.file_url = open('source/url_source.txt', 'a+')  # URL读取文件
        self.file_error = open('source/error.txt', 'a+')  # 日志错误记录
        self.file_log = None  # 日志常规记录

    def the_end(self):
        if self.file_url:
            self.file_url.close()
        if self.file_error:
            self.file_error.close()
        if self.file_log:
            self.file_log.close()


if __name__ == '__main__':
    mainAll()
