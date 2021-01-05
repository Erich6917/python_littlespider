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
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import util.file_check_util as file_util
from selenium.webdriver.chrome.options import Options

reload(sys)
sys.setdefaultencoding('utf-8')
hd_jump2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'player.videoincloud.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
hd_firefox = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'zip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'player.videoincloud.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
}


def search_real_url(url):
    # url = 'http://player.videoincloud.com/vod/3242311?src=gkw&cc=1'
    res = requests.get(url, headers=hd_jump2)
    # print res.text
    time.sleep(1)

    matcher = re.findall('src:\'(.+\.mp4)', res.text)
    if matcher:
        print 'ok'
        return str(matcher[0])
    print 'not found ', url


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
# url = 'http://player.videoincloud.com/vod/3246052?src=gkw&cc=1'
# url = 'http://player.videoincloud.com/vod/3244006?src=gkw&cc=1'
# print search_real_url(url)


def start_downlaod_local():
    file_mp4 = open('source_mp4.txt', 'a+')
    file_error_mp4 = open('error_mp4.txt', 'a+')
    with open('source/url_source.txt', 'a+') as file_source:
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


# start_downlaod_local()

def get_Chrome_options():
    chromeOpitons = Options()
    prefs = {
        "profile.managed_default_content_settings.images": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,

    }

    chromeOpitons.add_experimental_option('prefs', prefs)
    return chromeOpitons


# def search_real_url(driver):
#     download_href = driver.find_element_by_xpath(''
#                                                  '//video[@id="index_player_html5_api"]'
#                                                  '/source'
#                                                  '')
#     if download_href:
#         return download_href.get_attribute('src')


def start_telnet_jump_href():
    url_list = [
        # 'http://player.videoincloud.com/vod/3308264?src=gkw&cc=1',
        # 'http://player.videoincloud.com/vod/3308262?src=gkw&cc=1',
        # 'http://player.videoincloud.com/vod/3308199?src=gkw&cc=1',
        # 'http://player.videoincloud.com/vod/3308152?src=gkw&cc=1',
        # 'http://player.videoincloud.com/vod/3308110?src=gkw&cc=1',
        # 'http://player.videoincloud.com/vod/3308147?src=gkw&cc=1',
        'http://player.videoincloud.com/vod/3244006?src=gkw&cc=1',
    ]
    driver = webdriver.Chrome(chrome_options=get_Chrome_options())
    for url in url_list:
        # driver = webdriver.Chrome()
        driver.get(url)
        driver.set_page_load_timeout(20)

        print search_real_url(driver)
    driver.close()


def classification_flash_m3u8():
    file_list = file_util.get_all_files_path_name_endswith('source/jumps', '.txt')

    for file_name, file_path, file_root in file_list:
        # with open(file_path) as file_href:
        #     lines = file_href.readlines()
        #
        #     list_href = [line.replace('\n', '') for line in lines]

        output_root = file_root.replace('/jumps', '/player')
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        print 'source ', file_name, file_path

        list_href = open(file_path).readlines()

        output_path = os.path.join(output_root, 'source_init_success.txt')
        file_select = open(output_path, 'a+')
        output_error = os.path.join(output_root, 'source_init_m3u8.log')
        file_error = open(output_error, 'a+')
        for url_info in list_href:
            href = url_info.split('\t')[0]
            print 'telnet', href
            try:
                target_href = search_real_url(href)
            except Exception as e:
                print 'ERROR', href, e
                continue
            if target_href:
                # rt_list.append(target_href)
                file_select.write('{}\n'.format(target_href))
                file_select.flush()
            else:
                # rt_err.append(url_info)
                file_error.write(url_info)
                file_error.flush()

        if file_select:
            file_select.close()
        if file_error:
            file_error.close()


def search_m3u8_href(url):
    # url = 'http://player.videoincloud.com/vod/3306313?src=gkw&cc=1'
    req = requests.get(url, headers=hd_jump2)
    # print req.text
    matcher = re.search('encodeURIComponent\("([^)]+)"\)', req.text)
    time.sleep(1)
    if matcher:
        return matcher.group(1)
    else:
        print "error", url


def start_search_m3u8_href():
    file_list = file_util.get_all_files_path_name_endswith('source/player', '.log')

    for file_name, file_path, file_root in file_list:
        output_root = file_root.replace('/player', '/zone')
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        print 'source ', file_name, file_path

        list_href = open(file_path).readlines()

        output_path = os.path.join(output_root, 'zone_rt.txt')
        file_select = open(output_path, 'a+')
        output_error = os.path.join(output_root, 'zone_error.log')
        file_error = open(output_error, 'a+')
        for url_info in list_href:
            href, catalog_id = url_info.split('\t')[0], url_info.split('\t')[1]
            print 'telnet', href
            try:
                target_href = search_m3u8_href(href)
            except Exception as e:
                print 'ERROR', href, e
                continue
            if target_href:
                # rt_list.append(target_href)
                file_select.write('{}\t{}'.format(target_href, catalog_id))
                file_select.flush()
            else:
                # rt_err.append(url_info)
                file_error.write(url_info)
                file_error.flush()

        if file_select:
            file_select.close()
        if file_error:
            file_error.close()


# download_m3u8()
#
# start_telnet_jump_href()

# s1
classification_flash_m3u8()

# s2
start_search_m3u8_href()
