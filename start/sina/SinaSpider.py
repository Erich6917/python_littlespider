# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : finance.py
# @Commment: 新浪新闻页面整合处理
#

import re
import sys

import requests
import json
from bloom.sina.entity.newsEntity import pa_voice_news as newsEntity
import dateCheckUtil as dateUtil
import logger_util as logger
from bloom.sina.tools import sinaSoup as bSoup
from dbutil.DBNewsUtil import DBNews
from logger_util import infos

reload(sys)
sys.setdefaultencoding('UTF-8')

dbnews = DBNews()


def _finance_geturl_china(start=1, end=2):
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

    print 'page:', start, end
    for page in range(start, end):
        # post_param = {'pageid': '155', 'num': 10, 'page': page, 'lid': 1686}  # 1686
        post_param = {'pageid': '164', 'num': 10, 'page': page, 'lid': 1693}  # 产经
        req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        rtjson = json.loads(req.text)
        result = rtjson['result']
        data = result['data']
        # if True:
        #     # print rtjson
        #     print 'total:', result['total']
        #     return
        for ii in data:
            # print ii['url']
            p_url.append(ii['url'])
    return p_url


def _finance_geturl_world():
    """
    国际财经，只从首页上获取，其他为
    访问地址 http://finance.sina.com.cn/

    """
    baseurl = 'http://finance.sina.com.cn/world/'
    p_url = []

    data = requests.get(baseurl)  # print data
    regex = 'href="(https?://(?:finance.sina.com.cn|blog.sina.com.cn)/[^"]+)'
    result = re.findall(regex, data.text)
    for item in result:
        url = item
        print url
        # print chardet.detect(item[1])
        # print item[1], '>', item[2], '>', item[3]
        if url:
            p_url.append(url)
    return p_url


def sina_daily_sport_main_geturl():
    """

    :return:
    """
    scope = 'sports'
    url_list = []
    url_sport_main = 'http://sports.sina.com.cn/'
    soup = bSoup.soup_urlopen(url_sport_main)

    # other sports
    othersport = soup.select('.ppcs_l.fl')

    if not othersport:
        print '未定位到[综合体育]'

    for index in range(0, len(othersport)):
        alist = othersport[index].select('.list01 a')
        for a2 in alist:
            if a2.get("href"):
                print a2.get("href")
                url_list.append(a2.get("href"))

    return scope, url_list


def sina_finance_roll_getcount():
    """
    财经滚动  解析json内容
    访问地址 http://finance.sina.com.cn/roll/

    """
    baseurl = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?'
    'spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&r=0.9330196594434315'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               # "Content-Type": "application/json",
               "Accept": "*/*"}
    # post_param = {'col': '43', 'page': 1}
    # return_data = requests.get(baseurl, params=post_param, headers=headers, verify=False)
    # data = return_data.text
    # print data
    # 目测6827
    return 6827


def sina_finance_roll_geturl(start=1, end=2):
    """
    财经滚动  解析json内容
    访问地址 http://finance.sina.com.cn/roll/

    """
    baseurl = 'http://roll.news.sina.com.cn/interface/rollnews_ch_out_interface.php?'
    'spec=&type=&ch=03&k=&offset_page=0&offset_num=0&num=60&asc=&r=0.9330196594434315'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
               # "Content-Type": "application/json",
               "Accept": "*/*"}
    p_url = []
    print 'page:', start, end
    for page in range(start, end):
        post_param = {'col': '43', 'page': page}
        return_data = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        data = return_data.text

        #         print data
        result = re.findall('{channel : {title : (.+?),id : .*},title : "(.*)",url : "(.*)",type.*,time :(.*)},', data)
        for item in result:
            url = item[2]
            # print chardet.detect(item[1])
            # print item[1], '>', item[2], '>', item[3]
            if url:
                p_url.append(url)
    scope = 'finance'
    return scope, p_url


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

    p_finance_blog = r'http://blog.sina.com.cn/s/.*'  # sina blog

    p_finance_normal = r'http://finance.sina.com.cn/.*'  # sina finace normal type

    p_sports_normal = r'^http://sports.sina.com.cn/.*'

    # 结果返回字段
    rlist_entity = []
    num_exist = 0

    print '=============开始匹配=============== 初始请求条数', len(url_list), dateUtil.currDateFormate()

    for url in url_list:

        try:
            urlparam = {"news_url": url}
            isexist = dbnews.isexist_newsmsg(urlparam)
            if isexist:
                num_exist += 1
                continue
            if re.match(p_finance_normal, url, re.M):
                vmsg = sina_parse_artibody(url)
            elif re.match(p_sports_normal, url, re.M):
                vmsg = bSoup.parse_artibody(url)
            elif re.match(p_finance_blog, url, re.M):
                vmsg = sina_parse_finance_blog(url)
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


# 新浪博客内容获取
def sina_parse_finance_blog(url):
    return bSoup.parse_top_blog(url)


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


def sina_finance_thirdmarket_getcount():
    """
        财经新三板要闻
        访问地址 http://finance.sina.com.cn/stock/thirdmarket/

    """
    return 826


def sina_finance_thirdmarket_geturl(start=1, end=2):
    """
    财经新三板要闻
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
        post_param = {'channel': 'finance', 'show_num': 10, 'page': page, 'tag': 1
            , 'cat_1': 'zq1', 'cat_2': 'sbsc'}  # 产经
        req = requests.get(baseurl, params=post_param, headers=headers, verify=False)
        rtjson = json.loads(req.text)
        result = rtjson['result']
        data = result['data']
        for ii in data:
            print ii['url']
            p_url.append(ii['url'])
    scope = 'finance'
    return scope, p_url


def sina_finance_china_geturl(pageid, lid, start=1, end=2):
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

    print 'page:', start, end

    for page in range(start, end):
        # post_param = {'pageid': '155', 'num': 10, 'page': page, 'lid': 1686}  # 1686 财经-国内
        # pageid 155 财经国内,lid 1686 > 国内滚动,1687>宏观经济,1688>地方经济, 1690》金融新闻,1689>部委动态
        post_param = {'pageid': pageid, 'num': 10, 'page': page, 'lid': lid}  # 产经
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


def sina_finance_jj_jjyj_getcount():
    # 基金业界财经 > 基金 > 基金业界
    # 'http://roll.finance.sina.com.cn/finance/jj4/jjyj/index_262.shtml'
    # 暂定300 数据较老
    return 260


def sina_finance_jj_jjyj_geturl(start, end):
    # 基金业界财经 > 基金 > 基金业界
    # ‘http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index_5197.shtml
    url_list = []
    print 'page:', start, end
    for page in range(start, end):
        url = 'http://roll.finance.sina.com.cn/finance/jj4/jjyj/index_' + str(page) + '.shtml'
        soup = bSoup.soup_request(url)
        alist = soup.select('#Main .listBlk .list_009 a')
        for link in alist:
            # title = link.text
            url = link.get('href')
            # print link.text, link.get('href')
            if url:
                url_list.append(url)
    scope = 'finance'
    return scope, url_list


def sina_finance_jj_normal_getcount(types):
    # 基金声音 财经 > 基金 > 基金声音
    # 'http://roll.finance.sina.com.cn/finance/jj4/jjsy/index_300.shtml'
    # 暂定300 数据较老

    # ssgs   财经 > 证券 > 上市公司
    # zldx   财经 > 证券 > 主力动向
    # hgyj   财经 > 证券 > 宏观研究
    # gsjsy  财经 > 证券 > 股市及时雨
    # jjbk   财经 > 股票博客  > 基金博客
    # bkks   财经 > 股票博客  > 博客看市
    # qsyw   财经 > 期货 > 期市要闻
    # ncpzx  财经 > 期货 > 农产品资讯
    # pzyj   财经 > 期货 > 品种研究
    # ggggdp 财经 > 港股 > 港股个股点评
    # ggipo  财经 > 港股 > 港股IPO
    # gsxw   财经 > 港股 > 公司新闻
    # sdpl   财经 > 港股 > 深度评论
    # xgqzzx 财经 > 港股 > 香港权证资讯
    # jj4    财经 > 基金
    # jjsy   财经 > 基金 > 基金声音

    total = {
        'ssgs': 4990,  # ssgs   财经 > 证券 > 上市公司
        'zldx': 628,  # zldx   财经 > 证券 > 主力动向
        'hgyj': 445,  # hgyj   财经 > 证券 > 宏观研究
        'gsjsy': 5197,  # gsjsy  财经 > 证券 > 股市及时雨
        'jjbk': 580,  # jjbk   财经 > 股票博客  > 基金博客
        'bkks': 6710,  # bkks   财经 > 股票博客  > 博客看市
        'qsyw': 2100,  # qsyw   财经 > 期货 > 期市要闻
        'ncpzx': 3245,  # ncpzx  财经 > 期货 > 农产品资讯
        'pzyj': 1100,  # pzyj   财经 > 期货 > 品种研究
        'ggggdp': 1900,  # 财经  >  港股  >  港股个股点评
        'ggipo': 420,  # 财经 > 港股 > 港股IPO
        'gsxw': 4420,  # gsxw   财经 > 港股 > 公司新闻
        'sdpl': 188,  # 财经 > 港股 > 深度评论
        'xgqzzx': 615,  # 财经 > 港股 > 香港权证资讯
        'jj4': 3850,  # 财经 > 基金
        'jjsy': 300  # jjsy   财经 > 基金 > 基金声音

    }.get(types, 0)
    infos(types, '类型共计URL条数:', total)
    return total


def sina_finance_jj_normal_geturl(types, start, end):
    # 基金声音 财经 > 基金 > 基金声音
    # 财经 > 证券 > 股市及时雨 目测最多5200页
    # ‘http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index_5197.shtml
    url_list = []
    dic_url = {
        'ssgs': ['http://roll.finance.sina.com.cn/finance/zq1/ssgs/index_', '.shtml'],
        'zldx': ['http://roll.finance.sina.com.cn/finance/zq1/zldx/index_', '.shtml'],
        'hgyj': ['http://roll.finance.sina.com.cn/finance/zq1/hgyj/index_', '.shtml'],
        'gsjsy': ['http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index_', '.shtml'],
        'jjbk': ['http://roll.finance.sina.com.cn/blog/blogarticle/cj-jjbk/index_', '.shtml'],
        'bbks': ['http://roll.finance.sina.com.cn/blog/blogarticle/cj-bkks/inde_', '.shtml'],
        'qsyw': ['http://roll.finance.sina.com.cn/finance/qh/qsyw/index_', '.shtml'],
        'ncpzx': ['http://roll.finance.sina.com.cn/finance/qh/ncpzx/index_', '.shtml'],
        'pzyj': ['http://roll.finance.sina.com.cn/finance/qh/pzyj/index_', '.shtml'],
        'ggggdp': ['http://roll.finance.sina.com.cn/finance/gg/ggggdp/index_', '.shtml'],
        'ggipo': ['http://roll.finance.sina.com.cn/finance/gg/ggipo/index_', '.shtml'],
        'gsxw': ['http://roll.finance.sina.com.cn/finance/gg/gsxw/index_', '.shtml'],
        'sdpl': ['http://roll.finance.sina.com.cn/finance/gg/sdpl/index_', '.shtml'],
        'xgqzzx': ['http://roll.finance.sina.com.cn/finance/gg/xgqzzx/index_', '.shtml'],
        'jj4': ['http://roll.finance.sina.com.cn/finance/jj4/index_', '.shtml'],
        'jjsy': ['http://roll.finance.sina.com.cn/finance/jj4/jjsy/index_', '.shtml']
    }
    rt_dict = dic_url.get(types, [None, None])
    url_head, url_end = rt_dict[0], rt_dict[1]
    if not url_head:
        print '没对应路径'
        return url_head, url_end
    print 'page:', start, end
    for page in range(start, end):
        # url = 'http://roll.finance.sina.com.cn/finance/jj4/index_' + str(page) + '.shtml'
        url = url_head + str(page) + url_end
        soup = bSoup.soup_request(url)
        alist = soup.select('#Main .listBlk .list_009 a')
        for link in alist:
            # title = link.text
            url = link.get('href')
            # print link.text, link.get('href')
            if url:
                url_list.append(url)
    scope = 'finance'
    return scope, url_list


def telnet_finance_daily():
    """
        每次执行获取数据
    """
    rlist_entity = []

    scope, url_sports_main = sina_daily_sport_main_geturl()
    rlist_entity.extend(sina_parse_start(scope, url_sports_main))

    # if rlist_entity:
    #     dbnews.save_news_entity(rlist_entity)
    # else:
    #     logger.infos('no entity')


def telnet_finance_guonei():
    pageid = 155  # 国内财经
    # lids = [1686, 1687, 1688, 1689, 1690]
    # lids = [1687, 1688, 1689, 1690]
    lids = [1688, 1689, 1690]
    steps = 50
    for lid in lids:
        total = sina_finance_china_getcount(pageid, lid)
        pstart = 0
        while pstart < total:
            pend = pstart + steps
            scope, url_list = sina_finance_china_geturl(pageid, lid, pstart, pend)
            rlist_entity = sina_parse_start(scope, url_list)
            dbnews.save_news_entity(rlist_entity)
            pstart += steps


def telnet_finance_chanjing():
    # pageid = 164  # 财经-产经
    # lid
    # 1693 > 产经滚动,
    # 1694 > 公司新闻,
    # 1695 > 产业新闻,
    # 1696 > 深度报道,
    # 1697 > 人事变动

    pageid = 205  # 新股
    # lid
    # 1789 新股滚动
    # 1790 最新动态
    # 1791 新股评论
    # 1793 IPO中介
    # 1792 PE动态
    # lids = [1789, 1790, 1791, 1792, 1793]  # 完成

    # pageid = 384
    # lids = [2487] #外汇 pagenum 50
    pageid = 166  # 消费
    # lids
    # 1703 消费滚动
    # 1704 质量曝光
    # 1705 生活消费
    # 1706 企业召回
    # 1707 民生评论
    # 1708 小贴士
    lids = [
        # 1703,
        1704,
        # 1705, 1706, 1707, 1708
    ]

    steps = 50
    for lid in lids:
        total = sina_finance_china_getcount(pageid, lid)
        if total > 0:
            total = total / 10
        pstart = 51
        while pstart <= total - steps:
            pend = pstart + steps
            scope, url_list = sina_finance_china_geturl(pageid, lid, pstart, pend)
            rlist_entity = sina_parse_start(scope, url_list)
            dbnews.save_news_entity(rlist_entity)
            pstart += steps


def telnet_finance_roll():
    # 财经滚动 目测最多5200页

    steps = 10
    total = sina_finance_roll_getcount()
    pstart = 1
    while pstart < total:
        pend = pstart + steps

        scope, url_list = sina_finance_roll_geturl(pstart, pend)
        rlist_entity = sina_parse_start(scope, url_list)
        dbnews.save_news_entity(rlist_entity)
        pstart += steps


def telnet_finance_thirdmarket():
    # 新三板

    steps = 1
    total = sina_finance_thirdmarket_getcount()
    pstart = 1
    while pstart < total:
        pend = pstart + steps

        scope, url_list = sina_finance_roll_geturl(pstart, pend)
        rlist_entity = sina_parse_start(scope, url_list)
        dbnews.save_news_entity(rlist_entity)
        pstart += steps


def telnet_finance_jj_noraml():
    # types:
    # ssgs   财经 > 证券 > 上市公司
    # zldx   财经 > 证券 > 主力动向
    # hgyj   财经 > 证券 > 宏观研究
    # gsjsy  财经 > 证券 > 股市及时雨

    # jjbk   财经 > 股票博客  > 基金博客
    # bkks   财经 > 股票博客  > 博客看市
    # qsyw   财经 > 期货 > 期市要闻
    # ncpzx  财经 > 期货 > 农产品资讯
    # pzyj   财经 > 期货 > 品种研究
    # ggggdp 财经 > 港股 > 港股个股点评
    # ggipo  财经 > 港股 > 港股IPO
    # gsxw   财经 > 港股 > 公司新闻
    # sdpl   财经 > 港股 > 深度评论
    # xgqzzx 财经 > 港股 > 香港权证资讯
    # jj4    财经 > 基金
    # jjsy   财经 > 基金 > 基金声音

    steps = 10
    steps = 1
    type_list = ['ssgs', 'zldx', 'hgyj', 'gsjsy', 'jjbk', 'bkks', 'qsyw', 'ncpzx', 'pzyj', 'ggggdp', 'ggipo', 'gsxw',
                 'sdpl', 'xgqzzx', 'jj4', 'jjsy', ]

    # type_list = ['jj4']
    for types in type_list:
        total = sina_finance_jj_normal_getcount(types)
        pstart = 1
        while pstart <= total - steps:
            pend = pstart + steps
            scope, url_list = sina_finance_jj_normal_geturl(types, pstart, pend)
            if not scope:
                infos('异常中断，未找到对应类型')
                break
            rlist_entity = sina_parse_start(scope, url_list)
            dbnews.save_news_entity(rlist_entity)
            pstart += steps


def telnet_sports_football():
    # pageid = 43  # 欧冠首页滚动
    # lids = [307]

    pageid = 87  # 中国足球
    lids = [552]  # 全部

    pageid = 21  # 首页》中国足球 》中超
    lids = [203]

    pageid = 393  # 首页》中国足球》足金联赛》前方速递
    lids = [2532]
    steps = 10
    for lid in lids:
        total = sina_finance_china_getcount(pageid, lid)
        pstart = 0
        while pstart <= total - steps:
            pend = pstart + steps
            scope, url_list = sina_finance_china_geturl(pageid, lid, pstart, pend)
            scope = 'sports'
            rlist_entity = sina_parse_start(scope, url_list)
            dbnews.save_news_entity(rlist_entity)
            pstart += steps


def telnet_sports_noraml():
    """
        体育类型数据采集
    """
    # 欧冠 > 首页滚动
    # types:
    # ssgs   欧冠 > 首页滚动

    steps = 10
    type_list = ['']

    # type_list = ['jj4']
    for types in type_list:
        total = sina_finance_jj_normal_getcount(types)
        pstart = 1
        while pstart <= total - steps:
            pend = pstart + steps
            scope, url_list = sina_finance_jj_normal_geturl(types, pstart, pend)
            if not scope:
                infos('异常中断，未找到对应类型')
                break
            rlist_entity = sina_parse_start(scope, url_list)
            dbnews.save_news_entity(rlist_entity)
            pstart += steps


def telnet_tech_noraml():
    """
        新浪科技数据采集
    """
    # 欧冠 > 首页滚动
    # types:
    # ssgs   欧冠 > 首页滚动

    steps = 10
    type_list = ['']

    # type_list = ['jj4']
    for types in type_list:
        total = sina_finance_jj_normal_getcount(types)
        pstart = 1
        while pstart <= total - steps:
            pend = pstart + steps
            scope, url_list = sina_finance_jj_normal_geturl(types, pstart, pend)
            if not scope:
                infos('异常中断，未找到对应类型')
                break
            rlist_entity = sina_parse_start(scope, url_list)
            dbnews.save_news_entity(rlist_entity)
            pstart += steps


if __name__ == "__main__":
    startTime = dateUtil.currDateFormate()
    logger.infos('新浪网爬虫任务开始:', startTime)
    # finance
    # telnet_finance_daily()
    # telnet_finance_main()
    # telnet_finance_guonei()
    # telnet_finance_zhengquan_roll()
    # telnet_finance_roll()
    # telnet_finance_thirdmarket()

    # telnet_finance_jj_jjsy_roll()
    # telnet_finance_jj_jjyj_roll()
    telnet_finance_chanjing()
    # telnet_finance_jj_noraml()

    # telnet_sports_football()
    # daily
    # telnet_finance_daily()

    endTime = dateUtil.currDateFormate()

    print '新浪网处理完毕！', endTime
    print '本次共计耗时', (endTime - startTime)
