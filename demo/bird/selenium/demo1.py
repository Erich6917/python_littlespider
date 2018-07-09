# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 
# @Author  : LIYUAN134
# @File    : ControlNode.py
# @Commment: 
#            

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def open_baidu():
    browser = webdriver.Chrome()
    browser.get('http://www.baidu.com/')


def open_python_org():
    driver = webdriver.Chrome()
    driver.get('http:/www.python.org')

    assert 'Python' in driver.title
    elem = driver.find_element_by_name('q')
    elem.send_keys('pycon')
    elem.send_keys(Keys.RETURN)
    print driver.page_source


def open_js():
    phjs_path = "C:/Personal/WebApplication/python27/phantomjs-2.1.1-windows/bin/phantomjs.exe"
    driver = webdriver.PhantomJS(executable_path=phjs_path)
    # driver.get("http://www.baidu.com")
    driver.get("http://www.csdn.net")
    data = driver.title
    print data


def start_baidu():
    phjs_path = "C:/Personal/WebApplication/python27/phantomjs-2.1.1-windows/bin/phantomjs.exe"
    # driver = webdriver.PhantomJS(executable_path=phjs_path)
    driver = webdriver.Chrome()
    driver.get("http://www.baidu.com")
    # 标题定位
    print driver.title
    # 百度首页右上角的“新闻”，“hao123”，。。。。等等这些文字连接定位。就可以使用link text和partail link text定位方式
    print driver.find_element_by_link_text("新闻")
    print driver.find_element_by_link_text("贴吧")

    # 搜索框  输入搜索内容 然后触发
    key_search = u'今日中国'
    el_search = driver.find_element_by_xpath("//input[@id='kw']")
    el_search.send_keys(key_search)

    el_click = driver.find_element_by_xpath("//input[@id='su']")
    el_click.click()

    time.sleep(3)
    # driver.refresh()

    time.sleep(60)


def start_taobao():
    browser = webdriver.Chrome()
    browser.get("http://www.taobao.com")
    input_str = browser.find_element_by_id('q')
    input_str.send_keys("ipad")
    time.sleep(1)
    input_str.clear()
    input_str.send_keys("MakBook pro")
    button = browser.find_element_by_class_name('btn-search')
    button.click()


def start_runoob():
    browser = webdriver.Chrome()

    url = "http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable"
    browser.get(url)
    browser.switch_to.frame('iframeResult')
    source = browser.find_element_by_css_selector('#draggable')
    target = browser.find_element_by_css_selector('#droppable')
    actions = ActionChains(browser)
    actions.drag_and_drop(source, target)
    actions.perform()


def demo_forward():
    browser = webdriver.Chrome()
    browser.get('https://www.baidu.com/')
    browser.get('https://www.taobao.com/')
    browser.get('https://www.python.org/')
    browser.back()
    time.sleep(1)
    browser.forward()
    browser.close()


if __name__ == '__main__':
    demo_forward()
