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
    # 'Cookie': "_uab_collina=155435660766304150643617; acw_tc=76b20ff015543566239131760e6732ac0abb80b6a036506c7f5ec4e8c6b492; _uab_collina=155435665378754705870108; Hm_lvt_2e0edde4e3669a50ace26a2cddb33e60=1555061563; _pk_ref.1.a5e3=%5B%22%22%2C%22%22%2C1555165940%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSHaaIG5JZTKm02HKF2N_TpAKJDfFesWNDPeYJknWwEgyMPW8nDAd57dmbV0VyzqtmkPaNuJ3RlUoRkYzDFiqE_%26wd%3D%26eqid%3Da97c287800007118000000055ca5998d%22%5D; _pk_ses.1.a5e3=*; _pk_id.1.a5e3=3d60bc686bb0d63d.1554356608.7.1555165992.1555165940.; SERVERID=2666959f4331fe3ad439f4610ea751e3|1555166009|1555165944"

}
hd_jump2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'player.videoincloud.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    # 'Cookie': "_uab_collina=155435660766304150643617; acw_tc=76b20ff015543566239131760e6732ac0abb80b6a036506c7f5ec4e8c6b492; _uab_collina=155435665378754705870108; Hm_lvt_2e0edde4e3669a50ace26a2cddb33e60=1555061563; acw_sc__v3=5cb1ffeface93411573e9202ba34a1bfc4198683; acw_sc__v2=5cb2008c4805ddca6a19e618caa81447b5c445ca; _pk_ref.1.a5e3=%5B%22%22%2C%22%22%2C1555169417%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSHaaIG5JZTKm02HKF2N_TpAKJDfFesWNDPeYJknWwEgyMPW8nDAd57dmbV0VyzqtmkPaNuJ3RlUoRkYzDFiqE_%26wd%3D%26eqid%3Da97c287800007118000000055ca5998d%22%5D; _pk_ses.1.a5e3=*; _pk_id.1.a5e3=3d60bc686bb0d63d.1554356608.8.1555170714.1555169417.; SERVERID=2666959f4331fe3ad439f4610ea751e3|1555170720|1555165944"

}


def getCookie(url):
    response = requests.get(url, headers=hd)
    # print response.text
    cookie_value = ''
    for key, value in response.cookies.items():
        cookie_value += key + '=' + value + ';'
    return cookie_value
    # return response.cookies.get_dict()


def search_jump_url(url):
    cookie = getCookie(url)
    if True:
        return
    res = requests.get(url, headers=hd)
    rsoup = BeautifulSoup(res.text, 'html5lib')
    iframe = rsoup.select_one('iframe#player')
    if iframe:
        return iframe['src']
    else:
        print res.text


def soup_request(urls, coding='utf-8'):
    res = requests.get(urls)
    res.encoding = coding

    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(res.text, 'html5lib')
    return rsoup


def download_video_list():
    # catalogId, page_total = 2, 8981  # 刑事案件 label 11-20
    catalogId, page_total = 6, 1489  # 行政案件 label 21-23
    catalogId, page_total, label = 0, 46890, 2  # 民事 label 1-10
    # catalogId, page_total, label = 0, 924, 3  # 民事 label 1-10
    # catalogId, page_total, label = 0, 4874, 4  # 民事 label 1-10
    # catalogId, page_total, label = 0, 1162, 9  # 民事 label 1-10
    # catalogId, page_total, label = 0, 677, 8  # 民事 label 1-10
    # catalogId, page_total, label = 0, 216, 6  # 民事 label 1-10
    # catalogId, page_total, label = 0, 83, 5  # 民事 label 1-10
    # catalogId, page_total, label = 0, 45, 1  # 民事 label 1-10
    # catalogId, page_total, label = 0, 11, 10  # 民事 label 1-10
    # catalogId, page_total, label = 0, 46890, 10  # 民事 label 1-10
    page_size = 15
    page_total = (page_total / page_size)  #
    file_url = open('detail_minshi.txt', 'a+')
    for page_index in range(1, page_total):
        req_url = 'http://tingshen.court.gov.cn/search/a/revmor/full?' \
                  'keywords=&provinceCode=&cityCode=&label=&courtCode=&catalogId={}&dataType=5' \
                  '&pageSize=10&address=&timeFlag=&caseType=&courtType=' \
                  '&pageNumber={}&extType=&isOts='.format(catalogId, page_index)
        # url_main = 'http://tingshen.court.gov.cn/video'
        res = requests.get(req_url, headers=hd)
        try:
            # print res.text
            rt_json = json.loads(res.text)
            print 'telnet page', page_index
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


def start_download():
    # url = 'http://tingshen.court.gov.cn/live/5191388'
    file_rt = open('url_source.txt', 'a+')
    file_error = open('error.txt', 'a+')
    with open('url_telnet.txt', 'r+') as file_url:
        lines = file_url.readlines()
        for line in lines:
            try:
                url = line.replace('\n', '')
                url_jump = search_jump_url(url)
                if not url_jump:
                    file_error.write(line)
                    file_error.flush()
                    fail_msg = 'TEL ERROR \t{}'.format(url)
                    print fail_msg
                    continue

                url_real = search_real_url(url_jump)
                if url_real:
                    msg = '{}\n'.format(url_real)
                    file_rt.write(msg)
                    file_rt.flush()
                    time.sleep(0.2)
                else:
                    file_error.write(line)
                    file_error.flush()
                    fail_msg = 'TEL ERROR \t{}\t{}'.format(url, url_jump)
                    print fail_msg
            except Exception as e:
                file_error.write(line)
                file_error.flush()
                print 'Code err \t{}'.format(url), e


def search_real_url(url):
    # url = 'http://player.videoincloud.com/vod/3242311?src=gkw&cc=1'
    res = requests.get(url, headers=hd_jump2)
    time.sleep(1)

    matcher = re.findall('src:\'(.+\.mp4)', res.text)
    if matcher:
        return str(matcher[0])
        # else:
        #     print 'not match', url
        #     print res.text


def file_combine():
    file_target = open('url_telnet.txt', 'a+')

    with open('detail_minshi.txt', 'r+') as file_detail:
        lines = file_detail.readlines()
        for line in lines:
            arr_line = line.split('\t')
            video_id = arr_line[0]
            url = 'http://tingshen.court.gov.cn/live/{}\n'.format(video_id)
            file_target.write(url)


# start_download()
# url = 'http://tingshen.court.gov.cn/live/5195910'
# print search_jump_url(url)
# url = 'http://player.videoincloud.com/vod/3246052?src=gkw&cc=1'


def start_downlaod_local():
    file_mp4 = open('source_mp4.txt', 'a+')
    file_error_mp4 = open('error_mp4.txt', 'a+')
    with open('url_source.txt', 'a+') as file_source:
        lines = file_source.readlines()
        for line in lines:
            arr_line = line.replace('\n', '').split('\t')
            source_url, target_url = arr_line[0], arr_line[1]
            # print source_url, target_url
            source_mp4 = search_real_url(target_url)
            if not source_mp4:
                file_error_mp4.write(line)
                print 'error', target_url
            else:
                rt_msg = '{}\t{}\t{}\n'.format(source_url, target_url, source_mp4)
                file_mp4.write(rt_msg)
                print rt_msg

target_url = 'http://player.videoincloud.com/vod/3080304?src=gkw&cc=1'
print search_real_url(target_url)
# file_combine()
