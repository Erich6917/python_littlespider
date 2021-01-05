# -*- coding: utf-8 -*-
# @Time    : 2020-12-12
# @Author  : ErichLee ErichLee@qq.com
# @File    : CompanyDiscovery.py
# @Comment :
#

import time
import email_util
import requests
import random
from bs4 import BeautifulSoup
from selenium import webdriver

from util.file_check_util import *
from util.logger_util import *

reload(sys)
sys.setdefaultencoding('utf-8')

# city_all = ["zhenjiang", "changzhou", "wuxi", "xuzhou", "lianyungang", "huaian", "yancheng",
#             "yangzhou", "taizhou", "nantong", "suqian", "hefei", "bengbu", "wuhu", "huainan", "bozhou", "fuyang",
#             "huaibei", "suzhou", "chuzhou", "anqing", "chaohu", "maanshan", "xuancheng", "huangshan", "chizhou",
#             "tongling", "jiaxing", "huzhou", "ningbo", "jinhua", "wenzhou", "lishui", "shaoxing", "quzhou", "zhoushan",
#             "taizhou"]

city_all = [
    "suqian", "bengbu", "wuhu", "huainan", "bozhou", "fuyang",
    "chuzhou", "anqing", "maanshan", "xuancheng", "huangshan", "chizhou",
    "tongling", "wenzhou", "lishui", "quzhou", "zhoushan"]


def telnet(url):
    try:
        print url
        rt = requests.get(url)  # , headers=hd
        return BeautifulSoup(rt.content, 'html5')
    except Exception as e:
        errors('访问失败！{}'.format(e))


def time_sleep():
    return random.randint(1, 3)


def start_step1_find_company():
    for city in city_all:
        print 'city:'.format(city)
        tel_url = 'https://www.made-in-china.com/company-search/{}/C1/1.html'.format(city)
        soup = telnet(tel_url)
        page_text = soup.select_one("a.page-dis")
        # if page_text is None or page_text == '':
        #     # file_empty = open('city/{}_company.txt'.format(city), 'a')
        #     # file_empty.write('emtpy')
        #     # file_empty.close()
        #     # continue
        #     return
        if page_text is None or page_text == '':
            page_max = 5
        else:
            print '[{}]'.format(page_text)
            page_max = int(page_text.text.strip())
            # 只取10 页数据
            page_max = 10 if page_max > 10 else page_max;

        print city, page_max
        print 'start city {}'.format(city)
        file_company = open('city/{}_company.txt'.format(city), 'a')

        for index in range(1, page_max):
            tel_url = 'https://www.made-in-china.com/company-search/{}/C1/{}.html'.format(city, index)
            soup = telnet(tel_url)
            url_list = soup.select('h2.company-name a')

            msg_all = ''
            for each in url_list:
                print each.text.strip(), 'https:{}'.format(each['href'].strip())
                rt_msg = u'{}@@@{}\n'.format(each.text.strip(), 'https:{}'.format(each['href'].strip()))
                msg_all = msg_all + rt_msg

            time.sleep(time_sleep())
            file_company.write(msg_all)
            file_company.flush()
        file_company.close()
        print 'end city {}'.format(city)


def login(driver):
    url_home = 'https://login.made-in-china.com/sign-in/?baseNextPage=https%3A%2F%2Fweijunmould.en.made-in-china.com%2F'
    driver.get(url_home)
    username = '1065120559@qq.com'
    password = 'boluop1314'
    driver.find_element_by_xpath(
        ".//*[@id='logonInfo.logUserName']"). \
        send_keys(username)
    driver.find_element_by_xpath(
        ".//*[@id='logonInfo.logPassword']"). \
        send_keys(password)
    driver.find_element_by_xpath(
        ".//*[@id='sign-in-submit']").click()

    time.sleep(5)


def sway1(driver):
    info_list = driver.find_elements_by_xpath("//*[@class='info-cont-wp']"
                                              "/div[@class='item'][2]"
                                              "/div[@class='info']")
    telephone = ''
    try:
        telephone = info_list[0].text
    except:
        pass
    return telephone, ''


def sway2(driver):
    phone = ''
    mobile = ''
    try:
        phone = driver.find_element_by_xpath("//*[@class='contact-info']"
                                             "/div[@class='info-item'][4]"
                                             "/div[@class='info-fields']").text
        mobile = driver.find_element_by_xpath("//*[@class='contact-info']"
                                              "/div[@class='info-item'][5]"
                                              "/div[@class='info-fields']").text
    except:
        pass
    return phone, mobile


# city_all = [
#             "suqian", "bengbu", "wuhu", "huainan", "bozhou", "fuyang",
#            "chuzhou", "anqing", "maanshan", "xuancheng", "huangshan", "chizhou",
#             "tongling", "wenzhou", "lishui", "quzhou", "zhoushan"]

def start_step2_find_phones():
    driver = webdriver.Chrome()
    login(driver)
    # xuancheng
    for city in ["hefei"]:
        # city = 'yangzhou'
        print city
        file_company = open('phone/{}_company.txt'.format(city), 'r')

        file_phone = open('file/{}_phone.txt'.format(city), 'a')

        for company in file_company:

            company_name = company.strip().split('@@@')[0]
            url = company.strip().split('@@@')[1]
            if url.endswith('/360-Virtual-Tour.html'):
                url = url.replace('/360-Virtual-Tour.html', '/contact-info.html')
            elif url.endswith('.com'):
                url = url + '/contact-info.html'

            # url = 'https://yuanda-shelf.en.made-in-china.com/contact-info.html'
            try:
                driver.get(url)
            except:
                print '连接超时'
                continue

            telephone, mobile = sway1(driver)
            if telephone == '':
                telephone, mobile = sway2(driver)

            if telephone == '' or telephone.startswith("https"):
                print '需重新登录'
                email_util.send_email("重新登录")
                time.sleep(10)
                continue

            if mobile.startswith("https"):
                mobile = ''

            msg = u'Telephone:{}@@@Mobile:{}@@@Company:{}\n'.format(
                telephone,
                mobile,
                company_name
            )
            if mobile == '':
                continue
            print msg
            file_phone.write(msg)
            file_phone.flush()
            time.sleep(time_sleep())
        # driver.close()
        # return


# start_step1_find_company()
start_step2_find_phones()
