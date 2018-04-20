# -*- coding: utf-8 -*-
# @Time    : 2018/2/6 
# @Author  : LIYUAN134
# @File    : xpath_demo1.py
# @Commment: 
#            
from lxml import etree
import requests

"""
nodename	选取此节点的所有子节点。
/	从根节点选取。
//	从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
.	选取当前节点。
..	选取当前节点的父节点。
@	选取属性。
"""


def demo():
    html = requests.get('http://www.lzu.edu.cn').content.decode('utf-8')

    dom_tree = etree.HTML(html)

    links = dom_tree.xpath("//div[@id='nav']/ul/li")
    '''
        XPath解释
        //div[@id='nav']/ul/li 可以理解为三部分
        P1-//div[@id='nav']  选取id为nav的div元素节点,其中需要注意的是id前一定要加@符号，此外@href等具体的属性，都需要@前缀
        p2-/ul  /指的是根节点，跟在p1后面表示，紧接着p1儿子的节点，但不包含孙子辈（包含3 4 5...代）。
                # 但有时我们需要找到p1下所有的li，可能是儿子、也可能是孙子辈。只需将/调整为//即可
                即上述路径调整为//div[@id='nav']//li
    '''
    print len(links)
    for i in links:
        # msgs = i.xpath('a/text()')
        # msgs = i.xpath('a/@href | a/text()')
        # print msgs
        msgs = i.xpath('.//a/text()')
        if msgs:
            for msg in msgs:
                print msg,
            print
    '''
        文本获取：接上述表达式
        P1-遍历a标签的文本内容使用 a/text()，即在原有基础上 a标签之下的内容
        P2-同方式1，.//a/text(),即 在当前节点之下的所有a标签的文本
        解释如果写成//a/text() 又会回到根节点，不正确写法
        获取文本和连接写法例如：//div/a/@href    //div/a/text()
    '''


if __name__ == '__main__':
    demo()
