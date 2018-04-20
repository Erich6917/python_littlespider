# -*- coding: utf-8 -*-
# @Time    : 2018/3/26 
# @Author  : LIYUAN134
# @File    : YoukuDemo.py
# @Commment: 
#            
import urllib, urllib2, sys, os
from bs4 import BeautifulSoup
import itertools, re

url_i = 1
pic_num = 1


# 自己定义的引号格式转换函数
def _en_to_cn(str):
    obj = itertools.cycle(['“', '”'])
    _obj = lambda x: obj.next()
    return re.sub(r"['\"]", _obj, str)


def start():
    # 下载连续3个网页的视频
    url = 'http://v.youku.com/v_show/id_XMTI5NjE4MTk2OA==.html?spm=a2h0k.8191407.0.0'
    webContent = urllib2.urlopen(url)
    data = webContent.read()
    # 利用BeautifulSoup读取视频列表网页数据
    soup = BeautifulSoup(data)
    print "-------------------------Page " + str(url_i) + "-------------------------"
    # 获得相应页面的视频thumbnail和title的list
    tag_list_thumb = soup.findAll('li', 'v_thumb')
    tag_list = soup.findAll('li', "v_title")
    for item in tag_list:
        # 通过每个thumbnail中的herf导向视频播放页面
        web_video_play = urllib2.urlopen(item.a['href'])
        data_vp = web_video_play.read()
        # 利用BeautifulSoup读取视频播放网页数据
        soup_vp = BeautifulSoup(data_vp)
        # 找到“下载”对应的链接
        tag_vp_list = soup_vp.findAll('a', id='fn_download')
        for item_vp in tag_vp_list:
            # 将下载链接保存到url_dw中
            url_dw = '"' + item_vp['_href'] + '"'
            print item.a['title'] + ": " + url_dw
            # 调用命令行运行iku下载视频，需将iku加入环境变量
            os.system("iku " + url_dw)
    # 保存每个视频的thumbnail
    for item_thumb in tag_list_thumb:
        urllib.urlretrieve(item_thumb.img['src'], "c:\\ZDownload\\thumbnails\\" + str(pic_num) + "." +
                           _en_to_cn(item_thumb.img['title']) + ".jpg")
    print "--------------------------------------------------------------"
    print "--------Page " + str(url_i) + "'s video thumbnails have  been saved!"


if __name__ == '__main__':
    start()
