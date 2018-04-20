# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 
# @Author  : LIYUAN134
# @File    : tool.py
# @Commment: 
#            
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import re


# 处理页面标签类
class Tool:
    # 去除img标签,1-7位空格,&amp;nbsp;
    removeImg = re.compile('&lt;img.*?&gt;| {1,7}|&amp;nbsp;')
    # 删除超链接标签
    removeAddr = re.compile('&lt;a.*?&gt;|&lt;/a&gt;')
    # 把换行的标签换为\n
    replaceLine = re.compile('&lt;tr&gt;|&lt;div&gt;|&lt;/div&gt;|&lt;/p&gt;')
    # 将表格制表&lt;td&gt;替换为\t
    replaceTD = re.compile('&lt;td&gt;')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('&lt;br&gt;&lt;br&gt;|&lt;br&gt;')
    # 将其余标签剔除
    removeExtraTag = re.compile('&lt;.*?&gt;')
    # 将多行空行删除
    removeNoneLine = re.compile('\n+')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        x = re.sub(self.removeNoneLine, "\n", x)
        # strip()将前后多余内容删除
        return x.strip()

    def addUrlHead(self, url):
        if url:
            if url.startswith('http'):
                return url
            else:
                return 'https:' + url
