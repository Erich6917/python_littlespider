# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 
# @Author  : ErichLee ErichLee@qq.com
# @File    : voa51.py
# @Comment : 
#            

import sys
from bs4 import BeautifulSoup
import requests
import re
import os

reload(sys)
sys.setdefaultencoding('utf-8')


def soup_request(urls, coding='utf-8'):
    res = requests.get(urls)
    res.encoding = coding

    # 使用剖析器为html.parser
    rsoup = BeautifulSoup(res.text, 'html5lib')
    return rsoup


def download_url():
    main_url = 'http://www.51voa.com/Technology_Report_1.html'
    soup = soup_request(main_url)
    li_list = soup.select('div#left_nav ul:nth-of-type(2) li a')
    rt_url = []
    for li in li_list:
        name, href = li.text, 'http://www.51voa.com/{}'.format(li['href'])
        rt_msg = '{}@@@{}\n'.format(name, href)
        rt_url.append(rt_msg)
    with open('voa_url.txt', 'a+') as file_voa:
        file_voa.writelines(rt_url)


def get_page_sise(url):
    soup = soup_request(url)
    pg = soup.select_one('div#pagelist b:nth-of-type(2)')
    return int(pg.text)


def download_vedio(file_path, path):
    rt = requests.get(path)
    with open(file_path, 'wb') as file_audio:
        file_audio.write(rt.content)


def parse_detail(title, href):
    soup = soup_request(href)
    try:
        map3_path = soup.select_one('#menubar a#mp3')['href']  # 音频
        lrc_path = soup.select_one('#menubar a#lrc')['href']  # 字幕
        lrc_path = 'http://www.51voa.com/{}'.format(lrc_path)
        # print map3_path, lrc_path

        mp3_name = title + '.mp3'
        lrc_name = title + '.lrc'
        download_vedio(mp3_name, map3_path)
        download_vedio(lrc_name, lrc_path)
    except Exception as e:
        print 'ERROR,', href, e


def parse_page_url(href):
    soup = soup_request(href)
    li_list = soup.select('div#list ul li')
    rt_list = []
    for li in li_list:
        tag_imgs = li.find_all('img')
        if tag_imgs and len(tag_imgs) == 2:
            tag_a = li.select_one('a')
            title, href = tag_a.text, 'http://www.51voa.com/{}'.format(tag_a['href'])
            rt_msg = (title, href)
            # rt_msg = '{}@@@{}\n'.format(href, title)
            rt_list.append(rt_msg)
    return rt_list


def parse_content_url():
    with open('voa_url.txt', 'a+') as file_url:
        detail_list = file_url.readlines()
        for detail in detail_list:
            title, href = detail.split('@@@')[0], detail.split('@@@')[1].strip()
            print 'start ', href
            # url = 'http://www.51voa.com/This_is_America_1.html'
            page_size = get_page_sise(href)

            type_list = []
            for page in range(1, page_size + 1):
                print 'telnet page', page
                href_end = '_{}.html'.format(page)
                href = re.sub(re.compile(r"_[0-9]+.html", re.S), href_end, href)
                rt_page_list = parse_page_url(href)
                type_list.extend(rt_page_list)

            video_path = os.path.join('source', title)
            if not os.path.exists(video_path):
                os.mkdir(video_path)
            #
            print 'downloading... total', len(type_list)
            for each in type_list:
                title, href = each[0], each[1]
                name = os.path.join(video_path, title)
                parse_detail(name, href)

def clean_data():
    path_source = 'source'
    counter = 0
    for root, dirs, files in os.walk(path_source):
        for filename in files:
            print filename
            if filename.endswith('.mp3') or filename.endswith('.lrc'):
                pass
            else:
                os.remove(os.path.join(root, filename))
                counter += 1
    print path_source, '累计删除', counter


def start():
    download_url()
    parse_content_url()

    # clean_data()


start()
