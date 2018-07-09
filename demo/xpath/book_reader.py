# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 
# @Author  : ErichLee ErichLee@qq.com
# @File    : book_reader.py
# @Comment : 
#            

import sys
from lxml import etree
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


def demo1():
    path = 'book.xml'
    dom_tree = etree.parse(path)
    books = dom_tree.xpath("book/title/@name")

    for title in books:
        print title
        # print title.extract()

demo1()
