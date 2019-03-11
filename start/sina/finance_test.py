# -*- coding: utf-8 -*-
# @Time    : 2017/9/19
# @Author  : LIYUAN134
# @Site    :
# @File    : finance.py
# @Commment: 新浪财经板块
#

import sys

import chardet
import finance as finance

reload(sys)
sys.setdefaultencoding('UTF-8')


def test_one():
    # url = 'http://finance.sina.com.cn/china/gncj/2017-12-10/doc-ifypnqvn2337324.shtml'
    # url = 'http://finance.sina.com.cn/china/gncj/2017-12-10/doc-ifyppemf6155976.shtml'
    # url = 'http://finance.sina.com.cn/china/gncj/2017-12-08/doc-ifypnsip1013267.shtml'
    # url = 'http://finance.sina.com.cn/world/gjcj/2017-12-08/doc-ifyppemf5794576.shtml'
    # url = 'http://finance.sina.com.cn/7x24/2017-12-08/doc-ifypnqvn1402267.shtml'
    urls = []
    # urls.append('http://finance.sina.com.cn/stock/usstock/c/2017-12-12/doc-ifypnyqi4113880.shtml')
    # urls.append('http://finance.sina.com.cn/stock/usstock/c/2017-12-12/doc-ifypnyqi4313529.shtml')
    # urls.append('http://finance.sina.com.cn/china/gncj/2017-12-12/doc-ifyppemf6523068.shtml')
    # urls.append('http://finance.sina.com.cn/money/future/fmnews/2017-12-12/doc-ifypsvkp2208496.shtml')
    # urls.append('http://finance.sina.com.cn/stock/usstock/c/2017-12-12/doc-ifyppemf6523426.shtml')
    # urls.append('http://finance.sina.com.cn/money/future/fmnews/2017-12-12/doc-ifypnyqi4335810.shtml')
    #
    # urls.append('http://finance.sina.com.cn/stock/jsy/2017-12-12/doc-ifypnsiq0143844.shtml')
    # urls.append('http://finance.sina.com.cn/stock/usstock/c/2017-12-12/doc-ifypnyqi4115729.shtml')
    # urls.append('http://finance.sina.com.cn/stock/jsy/2017-12-12/doc-ifypnyqi4105120.shtml  ')
    # urls.append('http://finance.sina.com.cn/stock/usstock/c/2017-12-12/doc-ifypsvkp2204620.shtml')
    # urls.append('http://finance.sina.com.cn/stock/jsy/2017-12-12/doc-ifyppemf6490894.shtml')
    # urls.append('http://finance.sina.com.cn/stock/hyyj/2017-12-12/doc-ifypsvkp2205438.shtml')
    # urls.append('http://finance.sina.com.cn/stock/y/2017-12-12/doc-ifyppemf6497203.shtml')
    #
    # urls.append('http://finance.sina.com.cn/stock/usstock/c/2017-12-12/doc-ifyppemf6524363.shtml')
    # urls.append('http://finance.sina.com.cn/china/gncj/2017-12-12/doc-ifyppemf6491848.shtml')
    # urls.append('http://finance.sina.com.cn/stock/jsy/2017-12-12/doc-ifypnqvn3572177.shtml')
    # urls.append('http://finance.sina.com.cn/stock/hyyj/2017-12-12/doc-ifypnsiq0217695.shtml')  # ERROR
    # urls.append('http://finance.sina.com.cn/stock/gujiayidong/2017-12-12/doc-ifypnqvn3586007.shtml')
    # urls.append('http://finance.sina.com.cn/stock/stocktalk/2017-12-12/doc-ifyppemf6523573.shtml')
    # urls.append('http://finance.sina.com.cn/money/future/fmnews/2017-12-13/doc-ifypnyqi4309786.shtml')
    # urls.append('http://finance.sina.com.cn/money/future/fmnews/2017-12-12/doc-ifypnyqi4335794.shtml')
    urls.append('http://finance.sina.com.cn/money/future/fmnews/2017-12-12/doc-ifypnyqi4335821.shtml')
    # urls.append('http://finance.sina.com.cn/stock/s/2017-12-12/doc-ifypnyqi4136385.shtml')
    # urls.append('http://finance.sina.com.cn/stock/stocktalk/2017-12-12/doc-ifypnyqi4320985.shtml')
    # urls.append('http://finance.sina.com.cn/stock/marketresearch/2017-12-12/doc-ifypsvkp2205465.shtml')


    rdicts = {}
    # vmsg = finance_parse_top_blog(url)
    for url in urls:
        vmsg = finance.finance_parse_top_cj(url)
        print url
        print vmsg
        print '=========================================='
        rdicts[url] = vmsg
        print chardet.detect(vmsg)
        # scope = 'finance'
        # dbnews = DBNews()
        # dbnews.save_sina_telnet_result_byone(rdicts, scope)


test_one()
