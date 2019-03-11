# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : sinaSoup.py
# @Commment: 新浪娱乐版块
#
# coding=utf8

import re

from dbutil.DBNewsUtil import DBNews
from bloom.sina.tools import sinaSoup as bSoup


class SinaDisport(object):
    BASEURL = 'http://ent.sina.news.cn/'
    BASEURL = 'http://ent.sina.com.cn/'

    """
        滚动路径获取
    """

    def disport_geturl_roll(self):
        urllist = []

        soup = bSoup.soup_urlopen(self.BASEURL)

        #         娱乐头条
        gnxw = soup.select('#ty-top-ent0 .ty-card-type10-r a')

        rmsg = bSoup.parse_href(gnxw, '娱乐头条')
        if rmsg is not None:
            urllist.extend(rmsg)
        else:
            print '娱乐头条获取为空'

        print "Total:", len(urllist)
        return urllist

    """
        获取所有路径信息，策略访问页面，返回保存路径和内容
    """

    def disport_geturl_all(self):
        urllist = self.disport_geturl_roll()

        print '页面捕获完毕，共计收集到地址：FINAL:', len(urllist)

        p_kan = r'http://k.sina.news.cn/article_.*'
        p_main = r'http://ent.sina.news.cn/[a-zA-Z]{1,4}/.*'

        rdicts = {}
        print '=============开始匹配==============='

        for url in urllist:
            #         print ii
            if url is not None:

                # rdicts.has_key(url):
                if url in rdicts:
                    # 重复url，不再请求
                    continue
                if re.match(p_kan, url, re.M) is not None \
                        or re.match(p_main, url, re.M) is not None:
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

    # 入库保存
    def telnet_disport_main(self):

        rdicts = self.disport_geturl_all()
        scope = 'disport'

        dbnews = DBNews()
        dbnews.save_sina_telnet_result(rdicts, scope)
        print '新浪-财经板块处理完毕！'


if __name__ == "__main__":
    sports = SinaDisport()
    sports.disport_geturl_all()
    # sports.telnet_disport_main()
