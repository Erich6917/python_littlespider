# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : sports.py
# @Commment: 新浪科技版块
#
# coding=utf8


import re
import requests
import json
from dbutil.DBNewsUtil import DBNews
from bloom.sina.tools import sinaSoup as bSoup


class SinaTech(object):
    BASEURL = 'http://tech.sina.com.cn/'

    # 科技头条
    def tech_geturl_roll(self):
        url_list = []

        soup = bSoup.soup_head(self.BASEURL)

        #         中间概要
        middle = soup.select('.tech-mid .tech-news ul li a')
        #         热点·动态获取
        #         hot=tools.select('.cardlist-a__list')
        rmsg = bSoup.parse_href(middle, '今日头条科技')
        if rmsg is not None:
            url_list.extend(rmsg)
        else:
            print '今日头条科技获取为空'

        print "Total:", len(url_list)
        return url_list

    # 科技热点
    def tech_geturl_hot(self):
        """
        科技热点URL抓取
        访问地址 BASEURL 查看JSON请求

        """
        baseurl = 'http://cre.mix.sina.news.cn/api/v3/get?callback=jQuery1112071208500552263_1505885780282' \
                  '&cateid=1z&cre=tianyi&mod=pctech&merge=3&statics=1'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                                 "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                   # "Content-Type": "application/json",
                   "Accept": "*/*"}
        p_url = []

        post_param = {'length': '15', 'up': '5', 'down': 0
                      }
        return_data = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        msg = return_data.text

        # 正则剥离js数据
        # step1 去取外层 Jquery{}格式，拿到json格式数据
        pdata = re.findall('jQuery[^(]+\(\s*({.*})\);', msg)

        if len(pdata) > 0:
            pdata = pdata[0]
        else:
            print 'parse js error step1 '
            return

        # step2 data数据格式转换 json 格式数据 转换为字典类型
        obj = json.loads(pdata)

        data = obj['data']

        if len(data) > 0:
            # dataDic = data[0]
            print len(data)
            for single in data:
                # title = single['title']
                url = single['url']
                # print title, ':', url
                p_url.append(url)
        else:
            print 'parse js error step2 '
            return

        return p_url

    def tech_geturl_all(self):
        url_list = []
        url_roll = self.tech_geturl_roll()
        url_hot = self.tech_geturl_hot()

        url_list.extend(url_roll)
        url_list.extend(url_hot)
        print '页面捕获完毕，共计收集到地址：FINAL:', len(url_list)
        p_new = r'http://tech.sina.com.cn/[a-zA-Z]{1,4}/.*'

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

    def telnet_tech_main(self):

        rdicts = self.tech_geturl_all()
        scope = 'technology'
        dbnews = DBNews()
        dbnews.save_sina_telnet_result(rdicts, scope)
        print '新浪-科技板块处理完毕！'


if __name__ == "__main__":
    sports = SinaTech()
    sports.telnet_tech_main()
    # sports.tech_geturl_hot()
    # sports.tech_geturl_all()
#     sports.tech_parse_local(1)
#     sports.sport_parse_national(1)
#     sports.telnet_tech_main()
