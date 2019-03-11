# -*- coding: utf-8 -*-
# @Time    : 2018/1/23
# @Author  : LIYUAN134
# @File    : VipTianyan_ParseUrls_yuan.py
# @Comment:
#

import os
import random
import sys

from selenium import webdriver

from util.EmailSendUtil import send_emails
from util.dateCheckUtil import *

reload(sys)
sys.setdefaultencoding('UTF-8')


class mainAll(object):
    __path_urls = 'urls'
    __path_source = 'source'

    # self.__path_urls = self.getCurrentPath() + '/' + self.__path_urls
    # self.__path_source = self.getCurrentPath() + '/' + self.__path_source

    def __init__(self):

        self.url = 'https://www.tianyancha.com/login'
        self.username = '15105169560'
        # 15105169560 > Firefox杜
        # 18625955055 > Ie贾
        # 18761585189 > Chrome
        # 15996201796 > yue
        # 18014700157 > ze hao
        self.password = 'aaaaa888'
        self.driver = self.login()

        self.robot = True  # 初始化为true，表示可以正常爬取数据
        self.counter = 0  # 连续访问失败计数器
        self.file_company = None  # 目标文件
        self.file_error = None
        self.file_log = None
        try:
            self.init_path()

            self.start_logs()  # 开启日志

            self.parse_start()
        except Exception, e:
            self.infos('ERROR:')
            self.infos(e)
        finally:
            self.infos("ok,the work is done!")
            if self.file_log:
                self.file_log.close()
            if self.file_error:
                self.file_error.close()
            send_emails('天眼-ParseUrl-Erich!')

    def init_path(self):
        self.__path_urls = os.path.join(self.getCurrentPath(), 'urls')
        self.__path_source = os.path.join(self.getCurrentPath(), 'source')

        # __path_source 文件写入地址 需要创建
        # __path_urls 读取文件地址，为空直接报错,无须创建
        if not os.path.exists(self.__path_source):
            os.mkdir(self.__path_source)

    @staticmethod
    def getCurrentPath():
        if getattr(sys, 'frozen', False):
            apply_path = os.path.dirname(sys.executable)
        elif __file__:
            apply_path = os.path.dirname(__file__)
        return apply_path

    def start_logs(self):
        log_name = 'logs{}.log'.format(str(currYMD()))
        file_log_path = os.path.join(self.__path_source, log_name)
        self.file_log = open(file_log_path, 'a')
        self.file_log.write('==============START : {}==========\n'.format(str(currDateFormate())))

        file_error_path = os.path.join(self.__path_source, 'error.log')
        self.file_error = open(file_error_path, 'a')

    def login(self):
        """
            页面自动登录
        """
        driver = webdriver.Firefox()
        self.get_driver(driver, self.url)

        # 模拟登陆
        driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input"). \
            send_keys(self.username)
        driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input"). \
            send_keys(self.password)
        driver.find_element_by_xpath(
            ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]").click()
        self.sleeps()
        driver.refresh()
        return driver
        #  获取所有表格和表单

    def get_all_dirs(self, path_source):
        file_list = []
        for root, dirs, files in os.walk(path_source):
            for filename in dirs:
                file_list.append(filename)
        return file_list

    def parse_start(self):

        """
            读取文件URL
        """
        dir_list = self.get_all_dirs(self.__path_urls)
        for pav in dir_list:
            pav = pav.decode('gbk')
            path_pav = self.__path_urls + '/' + pav
            target_path = self.__path_source + '/' + pav
            if not os.path.exists(target_path):
                os.mkdir(target_path)

            for filename in os.listdir(path_pav):
                path_file = path_pav + '/' + filename
                target_file = target_path + '/' + filename
                try:
                    if self.robot:
                        self.file_company = open(target_file, 'a+')
                        self.start_telnet(path_file)
                    else:
                        self.errors('程序被检测，停止应用！')
                        return
                except Exception, e:
                    self.errors("ERROR>", target_file)
                    self.errors(e)
                finally:
                    if self.file_company:
                        self.file_company.close()

    def start_telnet(self, path_file):
        lastmsg = []
        with open(path_file) as files:
            urls = files.readlines()
            if urls:
                self.infos('START PARSE - ', path_file)
                lastmsg = self.parse_urls(urls)

                self.infos('END   PARSE - ', path_file)
            else:
                self.errors(path_file, "文件内容为空无须解析")

        if lastmsg:
            self.infos('写入剩余内容 TOTAL:', len(lastmsg))

            with open(path_file, "w") as lastfile:
                for msg in lastmsg:
                    lastfile.write(msg)
        else:
            self.infos('删除文件', path_file)
            os.remove(path_file)

    def parse_urls(self, urls):
        lastmsg = []
        if not self.robot:
            self.infos('身份暴露！不再继续访问')
            return lastmsg
        self.infos('解析条数TOTAL>', len(urls))
        for uu in urls:
            if self.robot:
                uu = uu.replace('\n', '')
                self.infos('Telnet ', uu)
                self.parse_tel_tianyan(uu)
            else:
                lastmsg.append(uu)
        self.infos('剩余解析URL条数', len(lastmsg))
        return lastmsg

    def parse_tel_tianyan(self, url):
        self.get_driver(self.driver, url)
        rt = self.get_page_details(self.driver, url)
        if rt is None:
            self.counter += 1
            self.errors("页面访问失败次数", self.counter)
            if self.counter > 10:
                self.dis_robot()
                return
        else:
            self.counter = 0
        self.sleeps()

    def save_url(self, url):
        self.savemsg(url + '\n')

    def get_driver(self, driver, url):
        counter = 0
        while True:
            try:
                counter += 1
                driver.get(url)
                return
            except Exception, e:
                self.errors(str(counter) + ' 访问连接失败>' + str(e) + '\n')
                if counter >= 5:
                    self.errors('放弃连接，尝试连接失败次数>' + str(counter) + '\n')
                    return
                time.sleep(5)

    @staticmethod
    def sleeps():
        time.sleep(random.randint(1, 4))

    def get_page_msg(self, driver, front):
        counter = 0
        while True:
            try:
                self.get_driver(self.driver, front)
                a_list = driver.find_elements_by_xpath(
                    # "//div[@id='web-content']/div/div/div/div/div/div/div['@class=header']/a"
                    "//div[@id='web-content']/div/div/div"
                    "/div[@class='result-list']"
                    "/div[@class='search-result-single ']"
                    "/div[@class='content']"
                    "/div[@class='header']/a")
                return a_list
            except Exception, e:
                counter += 1
                errMsg = '获取页面元素失败 次数[' + str(counter) + ']' + '\n'
                self.errors(errMsg)
                if counter > 2:
                    return None
                self.sleeps()

    def get_page_details(self, driver, front):
        try:
            a_list = self.get_page_msg(driver, front)

            if a_list:
                for a in a_list:
                    href = a.get_attribute("href")
                    name = a.text
                    msg = front.ljust(60) + '@' + str(href).ljust(50) + '@' + str(name) + '\n'
                    self.savemsg(msg)
            else:
                self.errors("ERROR页面已经被检测")
                return None
        except Exception, e:
            errMsg = '明细获取失败>' + front + '>' + str(e) + '\n'
            self.errors(errMsg)
            # self.dis_robot()
            # self.sleeps()
            return None
        return 'SUCCESS'

    def dis_robot(self):
        self.robot = False

    def savemsg(self, msg):
        self.file_company.write(msg)

    def infos(self, *args):
        if args:
            str_list = []
            for each in args:
                str_list.append(str(each))
            msg = ''.join(str_list)
            print msg
            self.file_log.write(msg + '\n')

    def errors(self, *args):
        if args:
            str_list = []
            for each in args:
                str_list.append(str(each))
            msg = ''.join(str_list)
            print msg
            self.file_log.write(msg + '\n')
            self.file_error.write(msg + '\n')


if __name__ == '__main__':
    mainAll()
