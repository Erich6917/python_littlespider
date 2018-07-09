# -*- coding: utf-8 -*-
# @Time    : 2017/12/27 
# @Author  : LIYUAN134
# @File    : QSBK.py
# @Commment: 
#            
__author__ = 'CQC'
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
from bs4 import BeautifulSoup
import requests


# 糗事百科爬虫类
class QSBK:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        # self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        self.cookie = '_xsrf=2|1113665b|32757988ad1b56bc339f7c3a061f977a|1514338646; _qqq_uuid_="2|1:0|10:1514338647|10:_qqq_uuid_|56:ZDAzN2FkMjkwNGY3YWZkNThiYzU0YmYyYTM0YzQxYTljNDNmZjJmYQ==|0c84bc929dd03eddf271455e7582aa64e807f0b7e861762e91f286974ff911d1"; ADEZ_BLOCK_SLOT=FUCKIE; ADEZ_ST=FUCKIE; ADEZ_Source=www.qiushibaike.com/hot/; __cur_art_index=6701; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1514338640,1514339590; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1514345014; _ga=GA1.2.1660563119.1514338645; _gid=GA1.2.54198147.1514338645; ADEZ_ASD=1; ADEZ_PVC=1026761-16-jboz2hf0'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent, 'Cookie': self.cookie}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None
        rsoup = BeautifulSoup(pageCode, 'html5lib')
        msgs = rsoup.select('.content')

        pageStories = []
        for msg in msgs:
            pageStories.append(msg.text)
            # print msg.text
        # pattern = re.compile('&lt;div.*?author"&gt;.*?&lt;a.*?&lt;img.*?&gt;(.*?)&lt;/a&gt;.*?&lt;div.*?' +
        #                      'content"&gt;(.*?)&lt;!--(.*?)--&gt;.*?&lt;/div&gt;(.*?)&lt;div class="stats.*?class="number"&gt;(.*?)&lt;/i&gt;',
        #                      re.S)
        # items = re.findall(pattern, pageCode)
        # # 用来存储每页的段子们
        # pageStories = []
        # # 遍历正则表达式匹配的信息
        # for item in items:
        #     # 是否含有图片
        #     haveImg = re.search("img", item[3])
        #     # 如果不含有图片，把它加入list中
        #     if not haveImg:
        #         replaceBR = re.compile('&lt;br/&gt;')
        #         text = re.sub(replaceBR, "\n", item[1])
        #         # item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间,item[4]是点赞数
        #         pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[4].strip()])
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 5:
                # 获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1

    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            input = raw_input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            # 如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            # print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" % (page, story[0], story[2], story[3], story[1])
            print story
            # print u"第%d页\t发布内容:%s\t" % (page, story[0])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                # 当前读到的页数加一
                nowPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
