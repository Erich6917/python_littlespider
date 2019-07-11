# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_download.py
# @Comment : 
#            

import sys
import re
import sys
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from util.file_check_util import *
from util.logger_util import *


class mainAll(object):
    __path_source = 'output'

    def __init__(self):

        self.file_url = None  # URL读取文件
        self.file_error = None  # 日志错误记录
        self.file_log = None  # 日志常规记录

        try:
            self.init()  # 初始化日志

            self.scrapy_start()

        except Exception as e:
            infos('异常退出！{}'.format(e))
        finally:
            self.the_end()

        print("ok,the work is done!")

    def write_error_url(self, err_msg):
        self.file_error.write(err_msg)
        self.file_error.flush()

    def scrapy_start(self):
        url_list = self.get_source_url()
        for url in url_list:

            try:
                # url = 'http://tingshen.court.gov.cn/live/5202044'
                url = 'http://tingshen.court.gov.cn/live/5251756'
                print 'telnet', url
                driver = self.login(url)
                if not driver:
                    errors('登录失败!', url)
                    err_msg = '{}\n'.format(url)
                    self.write_error_url(err_msg)
                    continue
                url_jump = self.search_jump_url(driver)

                if not url_jump:
                    print '获取是失败', url
                    err_msg = '{}\n'.format(url)
                    self.write_error_url(err_msg)
                else:
                    rt_msg = '{}\t{}\n'.format(url, url_jump)
                    self.file_url.write(rt_msg)
                    self.file_url.flush()

            except Exception as e:
                print url, e
                err_msg = '{}\n'.format(url)
                self.write_error_url(err_msg)
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
            driver = webdriver.Chrome()
            driver.set_page_load_timeout(20)
            driver.get(url)
            element = WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_id('player'))
            # driver.implicitly_wait(2)
            # time.sleep(0.5)
            return driver
        except Exception as e:
            print e

    def get_source_url(self):
        with open('url_telnet.txt', 'r+') as file_url:
            lines = file_url.readlines()

            rt_list = [line.replace('\n', '') for line in lines]
        return rt_list

    def init(self):
        self.file_url = open('url_source.txt', 'a+')  # URL读取文件
        self.file_error = open('error.txt', 'a+')  # 日志错误记录
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
#
# def search_jump_url(url):
#     if True:
#         return
#     res = requests.get(url, headers=hd)
#     rsoup = BeautifulSoup(res.text, 'html5lib')
#     iframe = rsoup.select_one('iframe#player')
#     if iframe:
#         return iframe['src']
#     else:
#         print res.text
#
#
# def search_real_url(url):
#     # url = 'http://player.videoincloud.com/vod/3242311?src=gkw&cc=1'
#     res = requests.get(url, headers=hd_jump2)
#     matcher = re.findall('src:\'(.+\.mp4)', res.text)
#     if matcher:
#         return str(matcher[0])
#
#
# def start_download(self):
#     # url = 'http://tingshen.court.gov.cn/live/5191388'
#     file_rt = open('url_source.txt', 'a+')
#     file_error = open('error.txt', 'a+')
#
#     with open('url_telnet.txt', 'r+') as file_url:
#         lines = file_url.readlines()
#         for line in lines:
#             try:
#                 url = line.replace('\n', '')
#                 url_jump = search_jump_url(url)
#                 if not url_jump:
#                     file_error.write(line)
#                     file_error.flush()
#                     fail_msg = 'TEL ERROR \t{}'.format(url)
#                     print fail_msg
#                     continue
#
#                 url_real = search_real_url(url_jump)
#                 if url_real:
#                     msg = '{}\n'.format(url_real)
#                     file_rt.write(msg)
#                     file_rt.flush()
#                     time.sleep(0.2)
#                 else:
#                     file_error.write(line)
#                     file_error.flush()
#                     fail_msg = 'TEL ERROR \t{}\t{}'.format(url, url_jump)
#                     print fail_msg
#             except Exception as e:
#                 file_error.write(line)
#                 file_error.flush()
#                 print 'Code err \t{}'.format(url), e
