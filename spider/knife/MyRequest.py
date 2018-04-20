# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 
# @Author  : LIYUAN134
# @File    : MyRequest.py
# @Commment: request 方法常用
#            

import requests
import re


def cookie_demo1():
    # 如果一个响应中包含了cookie，那么我们可以利用 cookies 变量来拿到
    url = 'https://www.taobao.com/markets/mm/mm2017'
    # rt = requests.get(url)
    # print rt.cookies

    # 另外可以利用 cookies 变量来向服务器发送 cookies 信息
    # <Cookie thw=cn for .taobao.com/>
    cookies = dict(thw='cn for .taobao.com')
    rt = requests.get(url, cookies=cookies)

    title = re.findall(u'<title>(.*?)</title>', rt.text)
    if title:
        print title[0]


def timeout_demo1():
    """
        注：timeout 仅对连接过程有效，与响应体的下载无关。
    """
    url = 'http://github.com'
    rt = requests.get(url, timeout=0.001)
    print rt.text


def session_qsbk1():
    """
        使用request直接访问，直接返回登录页面，且糗事百科不需要登录也能访问，
        我们需要的是session
    """

    url_qsbk = 'https://www.qiushibaike.com/'
    rt = requests.get(url_qsbk)
    print rt.text


def session_qsbk2():
    url_main = 'https://www.qiushibaike.com'
    session = requests.session()
    session.get(url_main)

    rt = session.get(url_main)
    print rt.text


def verify_ssl():
    """
        当设置为True时，访问12306失败，修改为False即可
    """
    r = requests.get('https://kyfw.12306.cn/otn/', verify=True)
    print r.text


def proxies_demo1():
    # 代理
    proxies = {
        "https": "https://"
    }
    url = ''
    r = requests.get(url, proxies=proxies)
