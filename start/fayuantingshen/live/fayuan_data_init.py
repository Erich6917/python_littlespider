# -*- coding: utf-8 -*-
# @Time    : 2019/4/4 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_video.py
# @Comment : 
#
import re
import sys

import os
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
    'Cookie': "acw_tc=76b20ff015543566239131760e6732ac0abb80b6a036506c7f5ec4e8c6b492; _uab_collina=155435665378754705870108; Hm_lvt_2e0edde4e3669a50ace26a2cddb33e60=1555061563; _pk_ref.1.a5e3=%5B%22%22%2C%22%22%2C1555484320%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSHaaIG5JZTKm02HKF2N_TpAKJDfFesWNDPeYJknWwEgyMPW8nDAd57dmbV0VyzqtmkPaNuJ3RlUoRkYzDFiqE_%26wd%3D%26eqid%3Da97c287800007118000000055ca5998d%22%5D; _pk_ses.1.a5e3=*; acw_sc__v2=5cb6dc3d2583add0988f6f614415357d7cb1244e; _pk_id.1.a5e3=3d60bc686bb0d63d.1554356608.20.1555487807.1555484320.; SERVERID=2666959f4331fe3ad439f4610ea751e3|1555487816|1555481796"

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

query_catalogId = [
    # '2',
    '6',
    # '1'
]  # 2 刑事案件 、6 行政案件 、0 民事案件
dict_province_code = {
    "beijing": "110000",
    # "tianjin": "120000",
    # "hebei": "130000",
    # "shanxi": "140000",
    # "neimeng": "150000",
    # "liaoning": "210000",
    # "jilin": "220000",
    # "heilongjiang": "230000",
    # "shanghai": "310000",
    # "jiangsu": "320000",
    # "zhejiang": "330000",
    # "anhui": "340000",
    # "fujian": "350000",
    # "jiangxi": "360000",
    # "shandong": "370000",
    # "henan": "410000",
    # "hubei": "420000",
    # "hunan": "430000",
    # "guangdong": "440000",
    # "guangxi": "450000",
    # "hainan": "460000",
    # "chongqing": "500000",
    # "sichuan": "510000",
    # "guizhou": "520000",
    # "yunnan": "530000",
    # "xizang": "540000",
    # "shanxi": "610000",
    # "gansu": "620000",
    # "qinghai": "630000",
    # "ningxia": "640000",
    # "xinjiang": "650000",
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


common_query_url = 'http://tingshen.court.gov.cn/search/a/revmor/full?keywords=' \
                   '&provinceCode={}&cityCode=&label=0&courtCode=' \
                   '&catalogId={}&dataType=2' \
                   '&pageSize=10&address=&timeFlag=&caseType=&courtType=' \
                   '&pageNumber={}&extType=&isOts='


def download_init_video_url():
    # 视频首页
    # http://tingshen.court.gov.cn/search/full?address=/page/review/screenPage&dataType=2&pageSize=10&provinceCode=110000
    # 查询条件 1、案件类型
    #         2、案件所在省份
    page_number = 1
    for catalogId in query_catalogId:
        for province, province_code in dict_province_code.items():

            url = common_query_url.format(province_code, catalogId, page_number)
            try:
                res = request_headers(url, headers=hd)
                if not res:
                    print 'telnet failed'
                    continue
                rt_json = json.loads(res.text)
                paging = rt_json['paging']
                total_count, page_total = paging['totalCount'], paging['pageTotal']
                page_max = 1000 if (page_total > 1000)  else page_total
                print catalogId, province, province_code, page_max, page_total, total_count
                time.sleep(3.5)
            except Exception as e:
                print e


def download_init_video_url_demo():
    # 视频首页 http://tingshen.court.gov.cn/video
    # 查询条件 1、案件类型
    #         2、案件所在省份
    url = 'http://tingshen.court.gov.cn/search/a/revmor/full?keywords=&provinceCode=110000&cityCode=&label=0&courtCode=&catalogId=1&dataType=2&pageSize=10&address=&timeFlag=&caseType=&courtType=&pageNumber=1493&extType=&isOts='
    try:
        res = request_headers(url, headers=hd)
        if not res:
            print 'telnet failed'
            return
        # print res.text


        rt_json = json.loads(res.text)
        paging = rt_json['paging']
        total_count, page_total = paging['totalCount'], paging['pageTotal']
        print total_count, page_total

        for each in rt_json['resultList']:
            print each['caseId'], each['title'], each['caseNo'], each['beginTime']

        time.sleep(1)
    except Exception as e:
        print e


def telnet_href(province_code, catalog_id, page_number):
    url = common_query_url.format(province_code, catalog_id, page_number)
    res = request_headers(url, headers=hd)
    if not res:
        print 'telnet failed'
        return
    if res.status_code == 200:
        rt_json = json.loads(res.text)
        # result info
        rt_list = []
        for each in rt_json['resultList']:
            msg = '{}\t{}\t{}\t{}\t{}\t{}\t{}\n' \
                .format(each['caseId'], each['title'],
                        each['caseNo'], each['beginTime'], province_code, catalog_id,
                        page_number)
            rt_list.append(msg)
        return rt_list


def create_init_select_url():
    source_path_init = 'source/source_init_counter.txt'

    # file_init_href = open('source/source_init_href.txt', 'a+')
    with open(source_path_init, 'a+') as source_file:
        lines = source_file.readlines()
        for line in lines:
            line_arr = line.split('\t')
            catalogId, province, province_code, page_total = line_arr[0], line_arr[1], line_arr[2], line_arr[3],
            print catalogId, province, province_code, page_total

            if "1" == catalogId:
                catalog_path = 'minshi'
            elif "2" == catalogId:
                catalog_path = 'xingshi'
            elif "6" == catalogId:
                catalog_path = 'xingzheng'
            else:
                print catalogId
                return

            writing_path = os.path.join('source/href', catalog_path, province)
            if not os.path.exists(writing_path):
                os.makedirs(writing_path)
            with open(os.path.join(writing_path, 'source_init_href.txt'), 'a+') as file_href:

                rt_list = []
                for page_number in range(1, (int(page_total) + 1)):
                    # query_url = "http://tingshen.court.gov.cn/search/a/revmor/full?keywords=" \
                    #             "&provinceCode={}&cityCode=-1&label=0&courtCode=-1" \
                    #             "&catalogId={}&dataType=5" \
                    #             "&pageSize=20&address=&timeFlag=0&caseType=&courtType=0" \
                    #             "&pageNumber={}&extType=&isOts="
                    url = '{}\t{}\t{}\t'.format(province_code, catalogId, page_number)
                    rt_list.append(url)
                file_href.writelines("\n".join(rt_list))

                # try:
                #     msg = telnet_href(catalogId, province, url)
                #     if msg:
                #         source_init_url.writelines(msg)
                #     else:
                #         print 'error', catalogId, province, url
                #     time.sleep(5)
                # except Exception as e:
                #     print e


def create_init_telnet_href():
    file_list = file_util.get_all_files_path_name('source/href')

    for file_name, file_path, file_root in file_list:
        with open(file_path) as file_href:
            lines = file_href.readlines()

            list_href = [line.replace('\n', '') for line in lines]
        # print file_name, file_path, len(list_href)

        output_root = file_root.replace('/href', '/infos')
        if not os.path.exists(output_root):
            os.makedirs(output_root)
        output_path = os.path.join(output_root, 'source_init_select.txt')
        print file_name, file_path, len(list_href), output_path
        file_select = open(output_path, 'a+')

        counter_err = 0
        for href_info in list_href:
            try:
                href_arr = href_info.split('\t')
                province_code, catalog_id, page_number = href_arr[0], href_arr[1], href_arr[2]
                print 'telnet...', province_code, catalog_id, page_number

                msg = telnet_href(province_code, catalog_id, page_number)
                if msg:
                    file_select.writelines(msg)
                    file_select.flush()
                else:
                    print '>>>>>>>>>>>>>>>>>>>>>>>>>>ERROR<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                time.sleep(5)
            except Exception as e:
                if counter_err > 10:
                    print "错误次数过多，程序关闭"
                    return
                counter_err += 1
                print e
                time.sleep(60)


# s1 下载个数
download_init_video_url()
download_init_video_url_demo()
# s2 按照省份 和 类型 创建对应的目录
create_init_select_url()

# s3 创建cateId
create_init_telnet_href()

# get_cookie_main()
