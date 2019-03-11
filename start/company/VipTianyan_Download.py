# -*- coding: utf-8 -*-
# @Time    : 2018/1/23
# @Author  : LIYUAN134
# @File    : demo.py
# @Comment:
#

import random

from selenium import webdriver

from util.dateCheckUtil import *
from util.file_check_util import *
from util.logger_util import *

reload(sys)
sys.setdefaultencoding('UTF-8')


class mainAll(object):
    __path_source = 'output'

    def __init__(self):
        self.url = 'https://www.tianyancha.com/login'
        self.username = '18751845189'  # 15105169560 > 杜
        self.password = 'aaaaa888'
        self.file_company = None  # 结果集文件
        self.file_url = None  # URL读取文件
        self.file_error = None  # 日志错误记录
        self.file_log = None  # 日志常规记录
        self.working = True

        try:
            self.init()

            self.scrapy_start()

        except Exception as e:
            infos('异常退出！{}'.format(e))
        finally:
            self.the_end()

        print("ok,the work is done!")

    def scrapy_start(self):
        driver = self.login()
        if not driver:
            errors('登录失败!')
            return

        path_url = os.path.join(self.__path_source, 'url')

        rt_list = self.get_urls(path_url)
        counter_error = 0
        for href in rt_list:

            company_detail = self.get_company_detail(driver, href)
            if company_detail:
                self.save_company(company_detail)
                self.sleeps()
                counter_error = 0
            else:
                self.errors('名称获取失败:{}'.format(href))
                counter_error += 1

                if counter_error > 10:
                    return

        driver.close()
        infos('>>> {}'.format(len(rt_list)))

    def get_company_detail(self, driver, href):
        infos('TELNET > {}'.format(href))
        self.get_driver(driver, href)
        try:
            # 获取title
            title = driver.find_element_by_xpath('//div[@class="header"]/h1[@class="name"]')
            title = title.text
            # 获取table明细
            xpath = '//div[@id="_container_baseInfo"]/table[2]/tbody'
            table = driver.find_element_by_xpath(xpath)
            code_register = table.find_element_by_xpath('tr[1]/td[2]').text  # 工商注册号
            code_organize = table.find_element_by_xpath('tr[1]/td[4]').text  # 组织机构代码
            code_identify = table.find_element_by_xpath('tr[3]/td[2]').text  # 纳税人识别号
            msg_eng_name = table.find_element_by_xpath('tr[7]/td[4]').text  # 英文名称
            msg_address = table.find_element_by_xpath('tr[8]/td[2]').text  # 注册地址
            rt_msg = '{0}@{1}@{2}@{3}@{4}@{5}\n' \
                .format(title
                        , code_register
                        , code_organize
                        , code_identify
                        , msg_eng_name
                        , msg_address)
            return rt_msg
        except Exception as e:
            errors('获取页面明细失败{}'.format(e))
            return

    @staticmethod
    def get_urls(path_url):
        files = get_all_files_path_name(path_url)
        rt_list = []
        for msg in files:
            name, path = msg[0], msg[1]
            with open(path, 'r') as target:
                messages = target.readlines()
                rt_url = [mess.split('@')[1].strip() for mess in messages]
            rt_list.extend(rt_url)
        return rt_list

    def init(self):
        # URL读取文件 路径
        path_url = os.path.join(self.__path_source, 'url')

        if not os.path.exists(path_url):
            errors('初始文件报错-未找到URL文件路径')
            return False
        # 结果集文件
        log_company_name = 'company_{}.txt'.format(currYMD())
        path_company = os.path.join(self.__path_source, log_company_name)
        self.file_company = open(path_company, 'a')

        # 日志文件夹
        path_log_base = os.path.join(self.__path_source, 'log')
        if not os.path.exists(path_log_base):
            os.mkdir(path_log_base)

        # 日志常规记录初始化
        log_name = 'log_{}.log'.format(currYMD())
        path_log = os.path.join(path_log_base, log_name)
        self.file_log = open(path_log, 'a')

        # 日志错误记录初始化
        path_error = os.path.join(path_log_base, 'error.log')
        self.file_error = open(path_error, 'a')

    def the_end(self):
        if self.file_company:
            self.file_company.close()
        if self.file_log:
            self.file_log.close()
        if self.file_error:
            self.file_error.close()

    def login(self):
        """
            页面自动登录
        """
        driver = webdriver.Chrome()
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
        time.sleep(3)
        driver.refresh()
        return driver
        #  获取所有表格和表单

    def get_driver(self, driver, url):
        counter = 0
        while True:
            try:
                counter += 1
                driver.get(url)

                time.sleep(1)

                return
            except Exception, e:
                self.errors(str(counter) + ' 访问连接失败>' + str(e) + '\n')
                if counter >= 2:
                    self.errors('放弃连接，尝试连接失败次数>' + int(counter) + '\n')
                    return
                time.sleep(10)

    def save_company(self, company_detail):
        self.file_company.write(company_detail)
        self.file_company.flush()

    @staticmethod
    def sleeps():
        time.sleep(random.randint(1, 3))

    def errors(self, *args):
        if args:
            str_list = []
            for each in args:
                str_list.append(str(each))
            msg = ''.join(str_list)
            print msg
            self.file_error.write(msg)

    def infos(self, *args):
        if args:
            str_list = []
            for each in args:
                str_list.append(str(each))
            msg = ''.join(str_list)
            print msg
            self.file_log.write(msg + '\n')


if __name__ == '__main__':
    mainAll()
    # send_emails('天眼任务搞定了!')
