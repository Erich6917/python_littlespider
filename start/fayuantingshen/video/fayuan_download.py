# -*- coding: utf-8 -*-
# @Time    : 2019/4/4 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_video.py
# @Comment : 
#
import re
import sys
import requests
import json
import time
from http import cookiejar
from bs4 import BeautifulSoup
from selenium import webdriver
import util.file_check_util as file_util

reload(sys)
sys.setdefaultencoding('utf-8')

hd = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'tingshen.court.gov.cn',
    'Referer': 'http://tingshen.court.gov.cn/video',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': "acw_tc=76b20ff015543566239131760e6732ac0abb80b6a036506c7f5ec4e8c6b492; _uab_collina=155435665378754705870108; Hm_lvt_2e0edde4e3669a50ace26a2cddb33e60=1555061563; acw_sc__v3=5cb69c397bb4c8e3e1a57902750ac0df0b2fbbac; acw_sc__v2=5cb69c399e8e6d8ce678f62cf317e2adcd7337ba; SERVERID=e5784715955cf8401e561e76eb6fd172|1555471523|1555471419; _pk_ref.1.a5e3=%5B%22%22%2C%22%22%2C1555471521%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSHaaIG5JZTKm02HKF2N_TpAKJDfFesWNDPeYJknWwEgyMPW8nDAd57dmbV0VyzqtmkPaNuJ3RlUoRkYzDFiqE_%26wd%3D%26eqid%3Da97c287800007118000000055ca5998d%22%5D; _pk_id.1.a5e3=3d60bc686bb0d63d.1554356608.19.1555471521.1555471521.; _pk_ses.1.a5e3=*"

}
hd_jump2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'player.videoincloud.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',

}

query_catalogId = ['2', '6', '0']  # 2 刑事案件 、6 行政案件 、0 民事案件
dict_province_code = {
    "beijing": "110000",
    "tianjin": "120000",
    "hebei": "130000",
    "shanxi": "140000",
    "neimeng": "150000",
    "liaoning": "210000",
    "jilin": "220000",
    "heilongjiang": "230000",
    "shanghai": "310000",
    "jiangsu": "320000",
    "zhejiang": "330000",
    "anhui": "340000",
    "fujian": "350000",
    "jiangxi": "360000",
    "shandong": "370000",
    "henan": "410000",
    "hubei": "420000",
    "hunan": "430000",
    "guangdong": "440000",
    "guangxi": "450000",
    "hainan": "460000",
    "chongqing": "500000",
    "sichuan": "510000",
    "guizhou": "520000",
    "yunnan": "530000",
    "xizang": "540000",
    "shanxi": "610000",
    "gansu": "620000",
    "qinghai": "630000",
    "ningxia": "640000",
    "xinjiang": "650000",
}


def request_headers(url, headers):
    session = requests.session()

    req = session.get(url, headers=headers)
    if req.status_code != 200:
        # print '访问失败',req.text
        print req
    return req


def get_cookie_main():
    url_main = 'http://tingshen.court.gov.cn/video'

    driver = webdriver.Chrome()
    driver.set_page_load_timeout(20)
    driver.get(url_main)

    cookie_list = driver.get_cookies()

    rt_list = []
    for cookie in cookie_list:
        # driver.add_cookie(cookie)
        # rt_list.append(cookie)
        # print type(cookie),cookie.get('name'),cookie.get('value')
        msg = '{}={};'.format(cookie.get('name'), cookie.get('value'))
        print msg

    time.sleep(10)
    print rt_list


def download_init_video_url():
    # 视频首页 http://tingshen.court.gov.cn/video
    # 查询条件 1、案件类型
    #         2、案件所在省份
    for catalogId in query_catalogId:
        for province, province_code in dict_province_code.items():
            query_url = "http://tingshen.court.gov.cn/search/a/revmor/full?keywords=" \
                        "&provinceCode={}&cityCode=-1&label=0&courtCode=-1" \
                        "&catalogId={}&dataType=5" \
                        "&pageSize=20&address=&timeFlag=0&caseType=&courtType=0" \
                        "&pageNumber=1&extType=&isOts="
            url = query_url.format(province_code, catalogId)
            try:
                res = request_headers(url, headers=hd)
                if not res:
                    print 'telnet failed'
                    continue
                rt_json = json.loads(res.text)
                paging = rt_json['paging']
                total_count, page_total = paging['totalCount'], paging['pageTotal']
                print catalogId, province, province_code, total_count, page_total
                time.sleep(1)
            except Exception as e:
                print e


def create_init_select_url():
    source_path_init = 'source/source_init_counter.txt'

    source_init_url = open('source/source_init_select.txt', 'a+')
    with open(source_path_init, 'a+') as source_file:
        lines = source_file.readlines()
        for line in lines:
            line_arr = line.split('\t')
            catalogId, province, province_code, total_count, page_total = line_arr[0], line_arr[1], line_arr[2], \
                                                                          line_arr[3], line_arr[4].replace('\n', '')
            print catalogId, province, province_code, total_count, page_total

            for page_number in range(25, int(page_total) + 1):
                query_url = "http://tingshen.court.gov.cn/search/a/revmor/full?keywords=" \
                            "&provinceCode={}&cityCode=-1&label=0&courtCode=-1" \
                            "&catalogId={}&dataType=5" \
                            "&pageSize=20&address=&timeFlag=0&caseType=&courtType=0" \
                            "&pageNumber={}&extType=&isOts="
                url = query_url.format(province_code, catalogId, page_number)

                try:
                    res = request_headers(url, headers=hd)
                    if not res:
                        print 'telnet failed'
                        continue
                    rt_json = json.loads(res.text)

                    # result info

                    print 'telnet page', catalogId, province, province_code, page_number
                    for each in rt_json['resultList']:
                        msg = '{}\t{}\t{}\t{}\t{}\t{}\n'.format(catalogId, province, each['caseId'], each['title'],
                                                                each['caseNo'], each['beginTime'])
                        source_init_url.write(msg)
                    time.sleep(5)
                except Exception as e:
                    print e


# download_init_video_url()
create_init_select_url()

# get_cookie_main()
