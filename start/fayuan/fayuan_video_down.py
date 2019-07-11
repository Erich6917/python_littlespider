# -*- coding: utf-8 -*-
# @Time    : 2019/4/4 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_video.py
# @Comment : 
#            

import sys
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


def download_video(url):
    url = 'http://121.28.48.74/ilive/nosecure/getSubVodUrlAction.action?assignId=7591C6CF_14A2_490A_ECC3_00507130E679&playType=2'
    url = 'http://player.videoincloud.com/vod/3181501?src=gkw&cc=1'
    res = requests.get(url)
    print res.text


def soup_request(urls, coding='utf-8'):
    res = requests.get(urls)
    res.encoding = coding

    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(res.text, 'html5lib')
    return rsoup


hd = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'tingshen.court.gov.cn',
    'Referer': 'http://tingshen.court.gov.cn/video',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': "acw_tc=76b20ff015543566239131760e6732ac0abb80b6a036506c7f5ec4e8c6b492; _uab_collina=155435665378754705870108; Hm_lvt_2e0edde4e3669a50ace26a2cddb33e60=1555061563; _pk_ref.1.a5e3=%5B%22%22%2C%22%22%2C1555123792%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSHaaIG5JZTKm02HKF2N_TpAKJDfFesWNDPeYJknWwEgyMPW8nDAd57dmbV0VyzqtmkPaNuJ3RlUoRkYzDFiqE_%26wd%3D%26eqid%3Da97c287800007118000000055ca5998d%22%5D; _pk_ses.1.a5e3=*; acw_sc__v3=5cb158ce572179ecf8b7de2ad988ac5c4a208d27; acw_sc__v2=5cb158cdb11d00e810a2995b8e598ef79ac2e209; _pk_id.1.a5e3=3d60bc686bb0d63d.1554356608.5.1555127240.1555123792.; SERVERID=2666959f4331fe3ad439f4610ea751e3|1555127249|1555117119"

}
import json
import time

def download_video_list():
    total = 58031
    page_size = 15
    page_total = (58031/15)-1
    file_url = open('rt_url_2.txt','a+')
    rt_list = []
    for page_index in range(101,102):
        req_url = 'http://tingshen.court.gov.cn/search/a/revmor/full?' \
                  'keywords=&provinceCode=&cityCode=&label=&courtCode=&catalogId=&dataType=5' \
                  '&pageSize=10&address=&timeFlag=&caseType=&courtType=' \
                  '&pageNumber={}&extType=&isOts='.format(page_index)
        # url_main = 'http://tingshen.court.gov.cn/video'
        res = requests.get(req_url, headers=hd)
        try:
            print res.text
            rt_json = json.loads(res.text)
            print 'telnet page',page_index
            for each in rt_json['resultList']:
                msg = '{}\t{}\t{}\t{}\n'.format(each['caseId'], each['title'], each['caseNo'], each['beginTime'])
                # rt_list.append(msg)
                file_url.write(msg)
            time.sleep(0.2)
        except Exception as e:
            print e
            continue
            # soup = soup_request(url_main)
            # soup = BeautifulSoup(res.text, 'html5lib')
            # print soup
            # print soup
            # a_list = soup.select('resultList')
            # #
            # for tag_a in a_list:
            #     print tag_a


download_video_list()
