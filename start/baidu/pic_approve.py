# -*- coding: utf-8 -*-
# @Time    : 2018/1/19 
# @Author  : LIYUAN134
# @File    : pic.py
# @Commment: 
#            

import os
import re
import urllib
import json
import socket
import requests
# 设置超时
import time
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 保存图片
    def __save_image(self, rsp_data, word):
        word = word.replace(' ', '')
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir('./' + word)) + 1
        print 'total', len(rsp_data['imgs'])

        for image_info in rsp_data['imgs']:
            try:
                time.sleep(self.time_sleep)
                fix = self.__get_suffix(image_info['objURL'])

                u = urllib.urlopen(image_info['objURL'])
                data = u.read()
                # word = 'aaa'
                file_name = str(word) + '/' + str(self.__counter) + str(fix)
                print file_name.decode('utf-8')
                f = open(file_name.decode('utf-8'), 'wb')
                f.write(data)
                f.close()

            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print("小黄图+1,已有" + str(self.__counter) + "张小黄图")
                self.__counter += 1
        return

    # 获取后缀名
    @staticmethod
    def __get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取前缀
    @staticmethod
    def __get_prefix(name):
        return name[:name.find('.')]

    # 开始获取
    def __get_images(self, word=u'美女'):
        # pn int 图片数
        pn = self.__start_amount
        while pn < self.__amount:

            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + word + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)

                # req = urllib.request.Request(url=url, headers=self.headers)
                # page = urllib.request.urlopen(req)
                # rsp = page.read().decode('unicode_escape')
                res = requests.get(url=url, headers=self.headers)
                res.encoding = 'UTF-8'
                rsp = res.text
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            except Exception as e:
                print '访问异常', url
            else:
                # 解析json
                rsp_data = json.loads(rsp)
                self.__save_image(rsp_data, word)
                # 读取下一页
                print("下载下一页")
                pn += 60
        print("下载任务结束")
        return

    def start(self, word, spider_page_num=1, start_page=1):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.__get_images(word)


if __name__ == '__main__':
    crawler = Crawler(0.05)
    # crawler.start('美女', 1, 2)
    # crawler.start(u'二次元 美女', 3, 3)
    crawler.start(u'文字', 1000, 7)
    # crawler.start('帅哥', 5)


def test_demo1():
    url = 'http://img4q.duitang.com/uploads/item/201309/29/20130929193101_MyMGt.png'
    # image = requests.get(url)
    u = urllib.urlopen(url)
    data = u.read()
    word = 'aaa'
    file_name = str(word) + '/' + '1.jpg'
    print file_name
    f = open(file_name, 'wb')
    f.write(data)
    f.close()
