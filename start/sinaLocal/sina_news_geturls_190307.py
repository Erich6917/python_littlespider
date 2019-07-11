# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : sina_news_geturls.py
# @Comment: 新浪新闻页面整合处理
#

import re
import sys
import os
import requests
import json
from newsEntity import pa_voice_news as newsEntity
import util.date_check_util as dateUtil
import util.logger_util as logger
from bs4 import BeautifulSoup
import sinaSoup as bSoup
from util.file_check_util import get_all_dirs, get_all_files
from util.logger_util import infos
import socket
import time

timeout = 5
socket.setdefaulttimeout(timeout)

reload(sys)
sys.setdefaultencoding('UTF-8')

gbl_path_source = 'source'
gbl_file_urls = None
gbl_file_log = None


def infos(*args):
    if args:
        global gbl_file_log
        str_list = []
        for each in args:
            str_list.append(str(each))
        msg = ''.join(str_list)
        print msg
        gbl_file_log.write(msg + '\n')


def current_path():
    """
        获取当前文件路径
        兼容pycharm和cmd直接运行脚本路径
    """
    if getattr(sys, 'frozen', False):
        apply_path = os.path.dirname(sys.executable)
    elif __file__:
        apply_path = os.path.dirname(__file__)
    return apply_path


def init_path():
    source = os.path.join(current_path(), gbl_path_source)
    if not os.path.exists(source):
        infos('Create path', source)
        os.mkdir(source)

    infos("Init Path...")


def init_files(filename='news_urls'):
    global gbl_path_source, gbl_file_urls, gbl_file_log
    source = os.path.join(current_path(), gbl_path_source)
    if not os.path.exists(source):
        os.mkdir(source)
    gbl_path_source = source

    if not gbl_file_log:
        gbl_file_urls = open(os.path.join(gbl_path_source, filename), 'a')
    if not gbl_file_log:
        file_logname = gbl_path_source + '\\logs' + str(dateUtil.curr_ymd()) + '.log'
        gbl_file_log = open(file_logname, 'a')
        infos("Create ", file_logname)
    infos("Init files...")


def close_files():
    global gbl_file_urls, gbl_file_log
    if gbl_file_urls:
        gbl_file_urls.close()
    if gbl_file_log:
        gbl_file_log.close()
    infos("Close files...")


def save_url(url):
    if url:
        global gbl_file_urls
        # print url
        gbl_file_urls.write(url + '\n')


def save_urls(url_list):
    if url_list:
        global gbl_file_urls
        gbl_file_urls.writelines(url_list)
        gbl_file_urls.flush()


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
    p_tech_old_normal = r'http://news.sina.com.cn/s/.*'  # sina finace normal type
    p_tech_normal = r'http://news.sina.com.cn/.*'  # sina finace normal type
    p_art_normal = r'http://cul.news.sina.com.cn/.*'
    # 结果返回字段
    rlist_entity = []
    num_exist = 0

    print '=============开始匹配=============== 初始请求条数', len(url_list), dateUtil.currDateFormate()
    for url in url_list:

        try:
            urlparam = {"news_url": url}
            isexist = True  # dbnews.isexist_newsmsg(urlparam)
            if isexist:
                num_exist += 1
                continue

            # if re.match(p_tech_old_normal, url, re.M):
            #     vmsg = bSoup.parse_news_art_normal(url)
            if re.match(p_tech_normal, url, re.M):
                vmsg = bSoup.parse_news_normal(url)
            elif re.match(p_art_normal, url, re.M):
                vmsg = bSoup.parse_news_normal(url)
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


def sina_news_china_geturl(pageid, lid, start=1, end=2, num=10):
    """
    """
    baseurl = 'http://feed.mix.sina.com.cn/api/roll/get?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Accept": "*/*"}
    p_url = []

    for page in range(start, end):
        post_param = {'pageid': pageid, 'num': num, 'page': page, 'lid': lid}  # 产经
        req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        rtjson = json.loads(req.text)
        result = rtjson['result']
        data = result['data']

        url = [msg['url'] for msg in data]
        p_url.extend(url)
        # for ii in data:
        #     p_url.append(ii['url'])
    return p_url


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
    scope = 'news'
    return scope, p_url


def sina_news_roll_main(pageid, lid):
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


def sina_news_geturl(types, start, end):
    url_list = []
    dic_url = {
        'gatxw': ['http://roll.news.sina.com.cn/news/gnxw/gatxw/index_', '.shtml'],
        'gdxw1': ['http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_', '.shtml'],
        'zs-pl': ['http://roll.news.sina.com.cn/news/gnxw/zs-pl/index_', '.shtml'],
        'gjmtjj': ['http://roll.news.sina.com.cn/news/gjxw/gjmtjj/index_', '.shtml'],
        'fz-shyf': ['http://roll.news.sina.com.cn/news/shxw/fz-shyf/index_', '.shtml'],
        'qwys': ['http://roll.news.sina.com.cn/news/shxw/qwys/index_', '.shtml'],
        'shwx': ['http://roll.news.sina.com.cn/news/shxw/shwx/index_', '.shtml'],
        'zgjq': ['http://roll.mil.news.sina.com.cn/col/zgjq/index_', '.shtml']
    }
    rt_dict = dic_url.get(types, [None, None])
    url_head, url_end = rt_dict[0], rt_dict[1]
    if not url_head:
        print '没对应路径'
        return url_head, url_end

    for page in range(start, end):
        # url = 'http://roll.finance.sina.com.cn/finance/jj4/index_' + str(page) + '.shtml'
        url = url_head + str(page) + url_end
        soup = bSoup.soup_request(url, 'gb2312')
        alist = soup.select('#Main .listBlk .list_009 a')
        for link in alist:
            # title = link.text
            url = link.get('href')
            # print link.text, link.get('href')
            if url:
                url_list.append(url)
    scope = 'news'
    return scope, url_list


def sina_news_getcount(types):
    # 959   财经 > 证券 > 上市公司

    total = {
        'gatxw': 959,  # 新闻中心 > 国内新闻 > 港澳台新闻
        'gdxw1': 10900,  # 新闻中心 > 国内新闻 > 各地新闻
        'zs-pl': 860,  # 新闻中心 > 国内新闻 > 综述分析
        'gjmtjj': 1500,  # 新闻中心 > 国际新闻 > 环球视野
        'fz-shyf': 1300,  # 新闻中心 > 社会新闻 > 社会与法
        'qwys': 350,  # 新闻中心 > 社会新闻 > 奇闻轶事
        'shwx': 4900,  # 新闻中心 > 社会新闻 > 社会万象
        'zgjq': 2000,  # 新闻中心 > 军事新闻 > 中国军事
    }.get(types, 0)
    infos(types, '类型共计URL条数:', total)
    return total


def telnet_news_roll():
    steps = 10
    type_list = ['gatxw', 'gdxw1', 'zs-pl']
    # 'zs-pl',
    # type_list = ['gatxw', 'gdxw1', 'zs-pl','gjmtjj','fz-shyf','qwys' ]
    # gatxw  新闻中心 > 国内新闻 > 港澳台新闻
    # gdxw1  新闻中心 > 国内新闻 > 各地新闻
    # zs-pl  新闻中心 > 国内新闻 > 综述分析
    # gjmtjj 新闻中心 > 国际新闻 > 环球视野
    # fz-shyf新闻中心 > 社会新闻 > 社会与法
    # qwys   新闻中心 > 社会新闻 > 奇闻轶事
    # shwx   新闻中心 > 社会新闻 > 社会万象
    # zgjq   新闻中心 > 军事新闻 > 中国军事

    max_counter = 5  # 最大空循环次数
    for types in type_list:
        total = sina_news_getcount(types)
        pstart = 1000
        while pstart <= total - steps:
            pend = pstart + steps

            print 'page:', '[', pstart, '-', pend, ']'
            scope, url_list = sina_news_geturl(types, pstart, pend)
            if not scope:
                infos('异常中断，未找到对应类型')
                break

            pstart += steps
            rlist_entity = sina_parse_start(scope, url_list)

            if not rlist_entity:
                # 如果连续多次结果集为空，则跳出循环
                if max_counter < 0:
                    max_counter = 5
                    infos('该访问规则多次访问未查询到内容')
                    break
                max_counter -= 1
                infos('URL抓取内容为空' + str(max_counter))
                continue

                # dbnews.save_news_entity(rlist_entity)


def telnet_news_normal():
    dic_lids = {
        # 已完成
        # 121: [1356],  # 首页》国内》最新新闻
        # 153: [2511],  # 滚动> 国际
        # 153: [2669],  # 滚动> 社会 #https://news.sina.com.cn/roll/#pageid=153&lid=2509&k=&num=50&page=1

    }

    # steps = 10
    page_size = 50
    for page_id, lids in dic_lids.items():
        for lid in lids:
            total = sina_finance_china_getcount(page_id, lid)
            p_start = 1
            page_total = total / page_size
            print 'Total {} , PageSize {} , Page {}'.format(total, page_size, page_total)

            while p_start <= page_total:
                pend = p_start + page_size

                url_list = sina_news_china_geturl(page_id, lid, p_start, pend, page_size)

                print 'telnet page[ {} > {} ] find > {}'.format(p_start, pend, len(url_list))
                save_urls('\n'.join(url_list))

                p_start += page_size


def sina_news_top_url_roll(pstart, pend):
    """
    各类型滚动
    http://roll.news.sina.com.cn/s/channel.php?ch=01#col=90,91,92
    &spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc=&page=1
    """
    baseurl = 'http://roll.news.sina.com.cn/s/channel.php?' \
              'ch=01#col=90,91,92&spec=&type=&ch=01&k=&offset_page=0&offset_num=0&num=60&asc='
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               "Accept": "*/*"}
    url_list = []
    for page in range(pstart, pend + 1):
        post_param = {'page': page}  # 产经
        req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        req.encoding = 'UTF8'
        soup = BeautifulSoup(req.text, 'html5lib')
        a_list = soup.select('#d_list ul li .c_tit a')
        for e_l in a_list:
            url_list.append(e_l.get('href'))

    return url_list


def sina_news_top_start():
    maxpage = 118
    steps = 10

    pstart = 1
    max_counter = 5
    while pstart <= maxpage - steps:
        pend = pstart + steps

        url_list = sina_news_top_url_roll(pstart, pend)

        scope = 'news'

        print 'page:', '[', pstart, '-', pend, ']'

        pstart += steps
        rlist_entity = sina_parse_start(scope, url_list)
        if not rlist_entity:
            # 如果连续多次结果集为空，则跳出循环
            if max_counter < 0:
                max_counter = 5
                infos('该访问规则多次访问未查询到内容')
                break
            max_counter -= 1
            infos('URL抓取内容为空' + str(max_counter))
            continue
            # dbnews.save_news_entity(rlist_entity)


def sina_news_ztlist_geturl(cat, start=1, end=2):
    """

        访问地址 http://finance.sina.com.cn/stock/thirdmarket/

    """
    baseurl = 'http://api.roll.news.sina.com.cn/zt_list?'
    # 'channel=finance&cat_1=zq1&cat_2=sbsc&show_ext=1&tag=1' \
    # '&callback=jQuery17206549982968638923_1513913697391&show_num=10&page=3&_=1513922919151'
    # baseurl = 'http://feed.mix.sina.com.cn/api/roll/get?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               # "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []

    print 'page:', start, end

    for page in range(start, end):
        # post_param = {'pageid': '155', 'num': 10, 'page': page, 'lid': 1686}  # 1686 财经-国内
        # pageid 155 财经国内,lid 1686 > 国内滚动,1687>宏观经济,1688>地方经济, 1690》金融新闻,1689>部委动态
        post_param = {'channel': 'news', 'show_num': 22, 'page': page, 'tag': 1
            , 'cat_1': cat, 'cat_2': '', 'show_all': 1}  # 产经
        req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        try:
            rtjson = json.loads(req.text)
            result = rtjson['result']
            data = result['data']
            for ii in data:
                p_url.append(ii['url'])
        except Exception, e:
            print '文本解析失败', e
    scope = 'news'
    return scope, p_url


def sina_parse_ztlist(cat, start=1, end=2):
    """

        访问地址 http://finance.sina.com.cn/stock/thirdmarket/

    """
    baseurl = 'http://api.roll.news.sina.com.cn/zt_list?'
    # 'channel=finance&cat_1=zq1&cat_2=sbsc&show_ext=1&tag=1' \
    # '&callback=jQuery17206549982968638923_1513913697391&show_num=10&page=3&_=1513922919151'
    # baseurl = 'http://feed.mix.sina.com.cn/api/roll/get?'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               # "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []

    print 'page:', start, end

    for page in range(start, end):
        # post_param = {'pageid': '155', 'num': 10, 'page': page, 'lid': 1686}  # 1686 财经-国内
        # pageid 155 财经国内,lid 1686 > 国内滚动,1687>宏观经济,1688>地方经济, 1690》金融新闻,1689>部委动态
        post_param = {'channel': 'news', 'show_num': 22, 'page': page, 'tag': 1
            , 'cat_1': cat, 'cat_2': '', 'show_all': 1}  # 产经
        try:
            req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
            rtjson = json.loads(req.text)
            result = rtjson['result']
            data = result['data']
            for ii in data:
                p_url.append(ii['url'])
        except Exception, e:
            print '文本解析失败', e
            time.sleep(10)
    return p_url


def geturls_news_china():
    # filename = 'news_china_2.txt'
    # init_files(filename)
    # init_path()

    dic_zlits = {
        # 'gnxw': 279263,
        # 'gnxw': 279,
        'shxw': 20000,  # 国内新闻 最新消息  3191
    }
    steps = 10
    pstart = 1
    counter = 0
    for cat, total in dic_zlits.items():
        print 'START', cat, total
        while pstart <= total - steps:
            pend = pstart + steps

            print 'page:', '[', pstart, '-', pend, ']'
            url_list = sina_parse_ztlist(cat, pstart, pend)
            if url_list:
                for url in url_list:
                    save_url(url)
            else:
                if counter > 10:
                    infos('停止URL获取')
                    return
                counter += 1
                infos('获取URL为空！', counter)
            time.sleep(1)
            pstart += steps
            # rlist_entity = sina_parse_start(scope, url_list)

    close_files()


# def sina_news_ztlist_start():
#     dic_zlits = {
#         # 'gnxw': 279263,
#         'shxw': 453606,  # 国内新闻 最新消息  3191
#     }
#     steps = 10
#     pstart = 5421
#     max_counter = 5
#     for cat, total in dic_zlits.items():
#         print 'START', cat, total
#         while pstart <= total - steps:
#             pend = pstart + steps
#
#             print 'page:', '[', pstart, '-', pend, ']'
#             scope, url_list = sina_news_ztlist_geturl(cat, pstart, pend)
#             if not scope:
#                 infos('异常中断，未找到对应类型')
#                 break
#
#             pstart += steps
#             rlist_entity = sina_parse_start(scope, url_list)
#
#             if not rlist_entity:
#                 # 如果连续多次结果集为空，则跳出循环
#                 if max_counter < 0:
#                     # max_counter = 5
#                     infos('该访问规则多次访问未查询到内容')
#                     break
#                 max_counter -= 1
#                 infos('URL抓取内容为空' + str(max_counter))
#                 continue
#             max_counter = 5
#             # dbnews.save_news_entity(rlist_entity)


if __name__ == "__main__":
    startTime = dateUtil.curr_date_format()
    logger.infos('新浪网爬虫任务开始:', startTime)
    filename = 'url_news_china_{}.txt'.format(dateUtil.curr_ymd_hms())
    init_files(filename)
    init_path()

    telnet_news_normal()
    # telnet_news_roll()
    # sina_news_top_start()
    # sina_news_ztlist_start()  # 接口API
    # geturls_news_china()  # 国内新闻

    endTime = dateUtil.curr_date_format()

    print '新浪网处理完毕！', endTime
    print '本次共计耗时', (endTime - startTime)
