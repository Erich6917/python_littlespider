# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : finance.py
# @Commment: 新浪体育新闻整合处理
#

import re
import sys

import requests
import json
from bloom.sina.entity.newsEntity import pa_voice_news as newsEntity
import dateCheckUtil as dateUtil
import logger_util as logger
from bloom.sina.tools import sinaSoup as bSoup
# from dbutil.DBNewsUtil import DBNews
import socket

timeout = 20
socket.setdefaulttimeout(timeout)
from logger_util import infos

reload(sys)
sys.setdefaultencoding('UTF-8')

# dbnews = DBNews()


def sina_parse_start(scope, url_list):
    """

    :param url_list: 需要解析的URL
    :return: 返回KEY > URL，Value > 捕获内容格式的信息
    """
    if not url_list:
        print '没有需要解析的URL'
        return []

    # URL 去重
    url_list = list(set(url_list))

    p_sports_normal = r'^https?://sports.sina.com.cn/.*'

    # 结果返回字段
    rlist_entity = []
    num_exist = 0

    print '=============开始匹配=============== 初始请求条数', len(url_list), dateUtil.currDateFormate()

    for url in url_list:

        try:
            # urlparam = {"news_url": url}
            # isexist = dbnews.isexist_newsmsg(urlparam)
            # if isexist:
            #     num_exist += 1
            #     continue

            if re.match(p_sports_normal, url, re.M):
                vmsg = sina_parse_artibody(url)
            else:
                print '暂未匹配该路径', url
                continue

            if vmsg:
                entity = newsEntity()
                entity.news_url = url
                entity.news_scope = scope
                entity.news_message = vmsg
                rlist_entity.append(entity)
                if len(rlist_entity) % 50 == 0:
                    print '已经获取记录数', len(rlist_entity), dateUtil.currDateFormate()
        except Exception, e:
            print '解析失败：', url, ':', e
            continue
    print '=============匹配结束===============', '本次采集数量：', len(rlist_entity), \
        '已存在记录:', num_exist, dateUtil.currDateFormate()

    return rlist_entity


# 财经首页内容获取
def sina_parse_artibody(url):
    return bSoup.parse_artibody(url)


'''获取新浪新闻根据请求地址获取信息入库 170905
'''


def sina_finance_china_getcount(pageid, lid):
    """
    访问地址 http://finance.sina.com.cn/china/
    # pageid 155 财经国内,
        lid 1686 > 国内滚动,
            1687>宏观经济,
            1688>地方经济,
            1690>金融新闻,
            1689>部委动态
    pageid 164 产经,
        lid 1693 > 产经滚动,
            1694>公司新闻,
            1695>产业新闻,
            1696>深度报道,
            1697>人事变动

    """
    baseurl = 'http://feed.mix.sina.com.cn/api/roll/get?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Accept": "*/*"}

    page = 1
    post_param = {'pageid': pageid, 'num': 10, 'page': page, 'lid': lid}  # 产经
    req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
    rtjson = json.loads(req.text)
    result = rtjson['result']
    if result['data']:
        print lid, '统计URL条数', result['total']
        return result['total']
    return 0


def sina_finance_china_geturl(pageid, lid, start=1, end=2, num=10):
    """
    国内财经，5sheet,5分页,10每页
    访问地址 http://finance.sina.com.cn/china/

    """
    baseurl = 'http://feed.mix.sina.com.cn/api/roll/get?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               # "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []

    print 'page:', '[', start, '-', end, ']', 'page_size:', num

    for page in range(start, end):
        # post_param = {'pageid': '155', 'num': 10, 'page': page, 'lid': 1686}  # 1686 财经-国内
        # pageid 155 财经国内,lid 1686 > 国内滚动,1687>宏观经济,1688>地方经济, 1690》金融新闻,1689>部委动态
        post_param = {'pageid': pageid, 'num': num, 'page': page, 'lid': lid}  # 产经
        req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        rtjson = json.loads(req.text)
        result = rtjson['result']
        data = result['data']
        # if True:
        #     # print rtjson
        #     print 'total:', result['total']
        #     return
        for ii in data:
            p_url.append(ii['url'])
    scope = 'finance'
    return scope, p_url


def telnet_tech_noraml():
    dic_lids = {
        43: [307, ],  # 体育》欧冠

    }
    max_counter = 100
    steps = 10
    page_size = 30

    file_sport = open('sport_20190114.txt','a+')
    for pageid, lids in dic_lids.items():
        for lid in lids:
            total = sina_finance_china_getcount(pageid, lid)
            pstart = 1
            page_total = total / page_size
            while pstart <= page_total:
                pend = pstart + steps
                scope, url_list = sina_finance_china_geturl(pageid, lid, pstart, pend, page_size)
                scope = 'sports'

                pstart += steps
                rlist_entity = sina_parse_start(scope, url_list)
                if not rlist_entity:
                    # 如果连续多次结果集为空，则跳出循环
                    if max_counter <= 0:
                        max_counter = 5
                        infos('该访问规则多次访问未查询到内容')
                        break
                    max_counter -= 1
                    infos('URL抓取内容为空'+str(max_counter))
                    continue
                for entity in rlist_entity:
                    file_sport.write(entity.news_message+'\n')
                file_sport.flush()
    file_sport.close()
                # dbnews.save_news_entity(rlist_entity)


if __name__ == "__main__":
    startTime = dateUtil.currDateFormate()
    logger.infos('新浪网爬虫任务开始:', startTime)

    telnet_tech_noraml()
    endTime = dateUtil.currDateFormate()

    print '新浪网处理完毕！', endTime
    print '本次共计耗时', (endTime - startTime)
