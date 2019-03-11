# -*- coding: utf-8 -*-
# @Time    : 2018/1/23
# @Author  : LIYUAN134
# @File    : demo.py
# @Commment:
#

import random
import sys
import os

from selenium import webdriver
from VipCoder import *
from util.dateCheckUtil import *
from util.EmailSendUtil import send_emails

reload(sys)
sys.setdefaultencoding('UTF-8')


class mainAll(object):
    __path_source = 'source'

    def __init__(self):
        self.url = 'https://www.tianyancha.com/login'
        # self.username = '15105169560'
        # self.password = 'aaaaa888'
        self.username = '18751845189'  # 15105169560 > 杜
        self.password = 'aaaaa888'
        self.word = u'淘宝'
        self.driver = self.login()
        self.file_company = None
        self.file_error = None
        self.file_log = None
        try:
            file_logname = 'source\\log_' + str(currYMD()) + '.log'

            if not os.path.exists('source'):
                os.mkdir('source')
            self.file_log = open(file_logname, 'a')
            self.file_log.write('START:' + str(currDateFormate()) + '..............\n')
            self.file_error = open('source\\error.log', 'a')
            self.scarpy_start(self.driver)
        except Exception, e:
            print 'ERROR:'
            print e
        finally:
            # self.file_company.close()
            self.file_log.close()
            self.file_error.close()
        print("ok,the work is done!")

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

    def scarpy_start(self, driver):

        """
            爬虫开始目录依次遍历 省》城市  然后遍历城市下行业分类、注册资本、注册时间、企业状态
        :param driver:
        """
        for province, citys in dic_city.items():
            self.infos('开始遍历省份 》', decode(province))
            for city in citys:
                # 每次城市创建一个文件编辑数据
                self.tel_city_trade(province, city, driver)

    def tel_city_trade(self, province, city, driver):
        """
            遍历每个城市的行业分类、注册资本、注册时间、企业状态
            如果小于5000，则直接访问,大于5000查询项细化
        """
        tel_url = 'https://%s.tianyancha.com/search/%s'
        counter = 0
        for trade in com_trade.keys():

            province_path = self.__path_source + '\\' + decode(province)
            if not os.path.exists(province_path):
                os.makedirs(province_path)
            file_name = province_path + '\\' + decode(city) + '_' + decode(trade) + '.txt'
            self.file_company = open(file_name, 'a')

            try:
                self.file_log.flush()

                content = decode(province) + '>' + decode(city) + '>' + decode(trade) + '>'
                url = tel_url % (city, trade)
                self.get_driver(driver, url)
                self.infos(content + url)
                counter += 1
                total = self.find_trade_total(driver)

                pages = self.find_trade_page(total)
                msg = str(counter) + ' ' + trade + ' total:' + str(total) + ' pages:' + str(pages)
                self.infos(msg)
                if self.is_resolve(total):
                    self.infos(content + u'查询开始：行业大类》行业明细》')
                    details = com_trade.get(trade)
                    self.tel_city_trade_details(city, details, content, driver)
                else:
                    front = content
                    self.infos(front + u'查询开始：行业大类》')
                    self.infos(front + u'信息获取保存中...')
                    self.get_page_details(driver, content)

                    for page in range(2, pages + 1):
                        url = tel_url % (city, (trade + '/p' + str(page)))
                        self.get_driver(driver, url)
                        front = content + 'page' + str(page)
                        self.infos(front + u'信息获取保存中...')
                        self.get_page_details(driver, front)

                self.file_company.close()
            except Exception, e:
                self.errors('行业分类遍历失败：' + str(e))
                self.file_company.close()

    def get_driver(self, driver, url):
        counter = 0
        while True:
            try:
                counter += 1
                driver.get(url)
                return
            except Exception, e:
                self.errors(str(counter) + ' 访问连接失败>' + str(e) + '\n')
                if counter >= 10:
                    self.errors('放弃连接，尝试连接失败次数>' + int(counter) + '\n')
                    return
                time.sleep(30)

    def tel_city_trade_details(self, city, details, content, driver):
        """
            大类明细
        """
        tel_url = 'https://%s.tianyancha.com/search/%s'
        for detail in details:
            url = tel_url % (city, detail)
            self.get_driver(driver, url)
            front = content + decode(detail) + '>'
            self.get_page_details(driver, front)

            total = self.find_trade_total(driver)
            pages = self.find_trade_page(total)
            msg = front + 'total:' + str(total) + ' pages:' + str(pages)
            self.infos(msg)
            if self.is_resolve(total):
                self.infos(front + u'查询开始：行业大类》行业明细》注册资金')
                # 注册资金
                vaules = com_values.keys()
                self.tel_city_trade_details_values(vaules, url, front, driver)

            else:
                self.infos(front + u'信息获取保存中...')
                self.get_page_details(driver, front)

                for page in range(2, pages + 1):
                    url = tel_url % (city, detail + '/p' + str(page))
                    self.get_driver(driver, url)
                    front = content + decode(detail) + '>page' + str(page)

                    self.infos(front + '信息获取保存中...')
                    self.get_page_details(driver, front)

    def tel_city_trade_details_values(self, values, urls, content, driver):
        for value in values:
            front = content + decode(value) + '>'
            url = urls + value
            self.get_driver(driver, url)
            total = self.find_trade_total(driver)
            pages = self.find_trade_page(total)
            msg = front + 'total:' + str(total) + ' pages:' + str(pages)
            self.infos(msg)
            if self.is_resolve(total):
                self.infos(front + u'查询开始：行业大类》行业明细》注册资金》注册时间')
                # 注册时间
                times = com_times.keys()
                self.tel_city_trade_details_values_times(times, url, front, driver)
            else:
                self.infos(front + u'信息获取保存中...')
                self.get_page_details(driver, front)
                self.sleeps()
                for page in range(2, pages + 1):
                    l_url = url + '/p' + str(page)
                    self.get_driver(driver, l_url)
                    front = content + decode(value) + '>page' + str(page)
                    self.infos(front + '信息获取保存中...')
                    self.get_page_details(driver, front)

    def tel_city_trade_details_values_times(self, times, urls, content, driver):
        for time in times:
            front = content + decode(time) + '>'
            url = urls + time
            self.get_driver(driver, url)
            total = self.find_trade_total(driver)
            pages = self.find_trade_page(total)
            msg = front + 'total:' + str(total) + ' pages:' + str(pages)
            self.infos(msg)
            if self.is_resolve(total):
                self.infos(front + u'查询开始：行业大类》行业明细》注册资金》注册时间》注册状态')
                # 注册状态
                status = com_status.keys()
                self.tel_city_trade_details_values_times_status(status, url, front, driver)
            else:
                self.infos(front + u'信息获取保存中...')
                self.get_page_details(driver, front)
                self.sleeps()
                for page in range(2, pages + 1):
                    l_url = url + '/p' + str(page)
                    self.get_driver(driver, l_url)
                    front = content + decode(time) + '>page' + str(page)
                    self.infos(front + '信息获取保存中...')
                    self.get_page_details(driver, front)

    def tel_city_trade_details_values_times_status(self, status, urls, content, driver):
        self.infos(content + u'信息获取保存中...')
        for stu in status:
            front = content + decode(stu) + '>'
            url = urls + stu
            self.get_driver(driver, url)
            total = self.find_trade_total(driver)
            pages = self.find_trade_page(total)
            msg = front + 'total:' + str(total) + ' pages:' + str(pages)
            self.infos(msg)
            for page in range(2, pages + 1):
                l_url = url + '/p' + str(page)
                self.get_driver(driver, l_url)
                front = content + decode(stu) + '>page' + str(page)
                self.infos(front + '信息获取保存中...')
                self.get_page_details(driver, front)

    @staticmethod
    def sleeps():
        time.sleep(random.randint(1, 4))

    def get_page_details(self, driver, front):
        try:
            a_list = driver.find_elements_by_xpath("//*[@id='web-content']/div/div/div/div/div/div/div/div/a")

            for a in a_list:
                href = a.get_attribute("href")
                name = a.find_element_by_tag_name('span').text
                msg = front.ljust(30) + '@' + str(href).ljust(50) + '@' + str(name) + '\n'
                self.savemsg(msg)
        except Exception, e:
            errMsg = '明细获取失败>' + front + '>' + str(e) + '\n'
            self.errors(errMsg)
        self.sleeps()

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
            self.file_error.write(msg)

    def find_trade_total(self, driver):
        """
                    获取行业下的总条数
        """
        list_title = driver.find_elements_by_xpath("//*[@id='web-content']/div/div/div/div/div/div/span/em")
        if list_title:
            try:
                msg = ''
                for title in list_title:
                    msg += title.text
                # print msg
                # total = int(list_title[1].text)
                total = int(msg)
                # self.infos('                  共计查询数据' + str(total))
            except Exception:
                self.errors('行业总条数获取失败：' + msg + '\n')
                return 0
            return total
        else:
            self.infos('============================================')
            self.infos('老铁你又被标记了!')
            self.infos('============================================')
        return 0

    @staticmethod
    def find_trade_page(total):
        """
            获取行业下的总页数
        """
        # 每页20条数据 普通会员100
        total_max = 5000
        page_size = 20
        page = total_max / page_size
        if total > total_max:

            return page
        else:
            page = total / page_size
            if total % page_size == 0:
                pass
            else:
                page += 1
        return page

    @staticmethod
    def is_resolve(total):
        return total > 5000


if __name__ == '__main__':
    mainAll()
    send_emails('天眼任务搞定了!')
    # import re
    # msg = '你好aaa，bbb'
    # pattern = "[\（\）\《\》\——\；\，\。\“\”\<\>\！]"  # 中文符号不够的自己加就行了
    # print re.sub(pattern, "", msg)
