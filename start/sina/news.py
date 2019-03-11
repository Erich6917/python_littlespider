# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : news.py
# @Commment: 新浪新闻版块
#
# coding=utf8

import re

from dbutil.DBNewsUtil import DBNews
from bloom.sina.tools import sinaSoup as bSoup


class SinaNews(object):
    # BASEURL = 'http://news.sina.news.cn/'
    BASEURL = 'http://news.sina.com.cn/'  # 2017-12-7 调整

    def news_geturl_roll(self):
        url_list = []

        soup = bSoup.soup_request(self.BASEURL)

        #         国内新闻
        gnxw = soup.select('#blk_new_gnxw .blk_09 ul li a')
        #         国际新闻
        gjxw = soup.select('#blk_gjxw_01 ul li a')
        #         社会新闻
        sh = soup.select('#blk_sh_01 ul li a')
        #         内地新闻
        ndxw = soup.select('#blk_ndxw_01 ul li a')
        #         军事新闻
        #         jsxw = tools.select('#blk_jsxw_02 ul li a')


        rurl = bSoup.parse_href(gnxw, '国内新闻')
        if rurl is not None:
            url_list.extend(rurl)
        else:
            print '国内新闻获取为空'

        rurl = bSoup.parse_href(gjxw, '国际新闻')
        if rurl is not None:
            url_list.extend(rurl)
        else:
            print '国际新闻获取为空'

        rurl = bSoup.parse_href(sh, '社会新闻')
        if rurl is not None:
            url_list.extend(rurl)
        else:
            print '社会新闻获取为空'

        rurl = bSoup.parse_href(ndxw, '内地新闻')
        if rurl is not None:
            url_list.extend(rurl)
        else:
            print '内地新闻获取为空'

        print "Total:", len(url_list)
        return url_list

    def news_geturl_all(self):
        url_list = self.news_geturl_roll()
        print '页面捕获完毕，共计收集到地址：FINAL:', len(url_list)

        p_new = r'http://news.sina.com.cn/[a-zA-Z]/.*'

        rdicts = {}
        print '=============开始匹配==============='

        for url in url_list:
            #         print ii
            if url is not None:

                if url in rdicts:
                    # 重复url，不再请求
                    continue
                if re.match(p_new, url, re.M) is not None:
                    vmsg = bSoup.parse_artibody(url)
                else:
                    print '暂未匹配该路径', url
                    continue

                if vmsg is not None:
                    rdicts[url] = vmsg
            else:
                print 'URL为None 跳过'
        print '结果集如下', len(rdicts)
        for k, v in rdicts.items():
            print k

        return rdicts

    # 保存到数据库
    def telnet_news_main(self):

        rdicts = self.news_geturl_all()
        scope = 'news'
        dbnews = DBNews()
        dbnews.save_sina_telnet_result(rdicts, scope)
        print '新浪-新闻板块处理完毕！'


if __name__ == "__main__":
    news = SinaNews()
    news.telnet_news_main()
    # news.news_geturl_all()

