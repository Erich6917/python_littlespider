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
    books_name = dom_tree.xpath(u"//book/title/text()")
    print 'all books name > {}'.format(books_name)

    book_children = dom_tree.xpath(u'//book[@category="CHILDREN"]')[0]

    print book_children
    print book_children.xpath('./author/text()')
    print book_children.xpath('./year/text()')

    print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
    print dom_tree.xpath(u'//book/author/text()')




demo1()
