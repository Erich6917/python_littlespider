# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 
# @Author  : LIYUAN134
# @File    : woziku.py
# @Commment: 我字酷 http://www.woziku.com/  字体下载
#            
import os
import re
import sys
import urllib
import socket
import requests
import os
from bs4 import BeautifulSoup

from util.dateCheckUtil import *
from util.logger_util import infos

reload(sys)
sys.setdefaultencoding('UTF-8')
socket.setdefaulttimeout(60)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome' \
                         '/61.0.3163.79 Safari/537.36'}

path_curr = u''
path_base = u'source/完结字体'
counter = 0
file_types = None
# file_path = 'source/url_complete.txt'
file_source = u'source'
file_path = os.path.join(file_source, 'url_ok.txt')
file_err = os.path.join(file_source, 'error.log')


def __get_suffix(name):
    """
        路径解析
    """
    m = re.search(r'\.[^\.]*$', name)
    if m.group(0) and len(m.group(0)) <= 5:
        return m.group(0)
    else:
        return '.jpeg'


def save_pic(url_image, title):
    global counter
    counter = counter + 1

    name_url = __get_suffix(url_image)

    image_name = path_curr + '/' + str(counter) + name_url
    f_image = open(image_name, 'wb')

    msg_name = path_curr + '/' + str(counter) + '.txt'
    f_txt = open(msg_name, 'wb')
    try:
        # step1 获取文件内容写入图片
        u = urllib.urlopen(url_image)
        image = u.read()
        f_image.write(image)

        # step2 写入文本
        f_txt.write(title)
    except Exception, e:
        f_err = open(file_err, 'a')
        err_msg = '文本保存失败,' + str(url_image) + '\n'
        f_err.write(err_msg)
        f_err.close()
    finally:
        f_image.close()
        f_txt.close()


def tel_types_detail(urls):
    s = requests.Session()
    res = s.get(urls, verify=False, headers=headers)
    rtmsg = res.text
    rsoup = BeautifulSoup(rtmsg, 'html5lib')
    grids = rsoup.select('.grid')
    for grid in grids:
        url_img = grid.select('.imgholder a img')[0]['src']
        title = grid.select('.tool')[0].text
        title = re.sub('\s', '', title)
        save_pic(url_img, title)


def tel_types_main(urls):
    s = requests.Session()
    res = s.get(urls, verify=False, headers=headers)
    rtmsg = res.text
    rsoup = BeautifulSoup(rtmsg, 'html5lib')
    # 查询标题
    try:
        title = rsoup.select('.panel-title a')[0].text
    except:
        infos('ERROR,获取标题失败：', urls)
        return
    global path_curr, path_base, counter
    path_curr = path_base + '/' + title.decode('utf-8')

    if not os.path.exists(path_curr):
        os.makedirs(path_curr)
        infos('该字体目录不存在，创建新目录！')
    else:
        infos('该字体目录已经存在不再重复下载！')
        return
    counter = len(os.listdir(path_curr))

    pattern = re.match('.*/t_([0-9]+).*', urls)
    if pattern:
        ids = pattern.group(1)
    else:
        infos('ERROR,id获取失败：', urls)
        return
    infos('目录', path_curr, '字体标识', ids)

    #
    comment = rsoup.select('#comments')
    size_each = 36  # 每页个数为36
    if comment:
        msg = comment[0].text
        pattern = re.match('[^0-9]*([0-9]+).*', msg)
        if pattern:
            total = pattern.group(1)
            total = int(total)
            page_size = total / size_each
            if total % 36 == 0:
                pass
            else:
                page_size += 1
            print 'total', total, 'page_size', page_size, '开始批量保存,请耐心等待...'
            for page in range(1, page_size + 1):
                if page == 1:
                    s_url = urls
                else:
                    s_url = 'http://www.woziku.com/topic/show/' + str(ids) + '/' + str(page)
                infos('page', page, '处理中...')
                try:
                    tel_types_detail(s_url)
                except Exception, e:
                    infos('分页字体保存失败!', s_url, e)
            print '批量保存完毕！'
        else:
            '尚未匹配', msg
    else:
        infos('字体个数获取失败')


def get_url_okwrite():
    # 写完
    # urls = ['http://www.woziku.com/t_okwrite.html', ]
    # 已完成字体
    urls = ['http://www.woziku.com/t_okttf.html', ]

    for url in urls:
        print '=================='
        s = requests.Session()
        res = s.get(url, verify=False, headers=headers)
        rtmsg = res.text
        rsoup = BeautifulSoup(rtmsg, 'html5lib')
        a_list = rsoup.select('#topic_list li h2 a')
        for a in a_list:
            print a.text, a['href']
            url = str(a['href']) + '\n'
            file_types.write(url)


def get_url_okwrite_more():
    urls = ['http://www.woziku.com//home/getmore_okttf/2',
            'http://www.woziku.com//home/getmore_okttf/3']
    for url in urls:
        print '=================='
        print url
        s = requests.Session()
        res = s.get(url, verify=False, headers=headers)
        rtmsg = res.text
        rsoup = BeautifulSoup(rtmsg, 'html5lib')
        a_list = rsoup.select('.media-body .media-heading.topic-list-heading a')
        for a in a_list:
            print a.text, a['href']
            url = str(a['href']) + '\n'
            file_types.write(url)


def download_types():
    try:
        global file_source, file_types
        if not os.path.exists(file_source):
            infos('dir source')
            os.mkdir(file_source)
        file_types = open(file_path, 'w+')
        get_url_okwrite()
        get_url_okwrite_more()
    except Exception, e:
        infos("ERROR", e)
    finally:
        file_types.close()


def check_url_isexist():
    """
        检查是否存在url目录，不存在则下载
    """
    if not os.path.exists(file_path):
        download_types()


def find_all_urls():
    file_url = open(file_path, 'r')
    lines = file_url.readlines()

    r_urls = []
    for line in lines:
        r_urls.append(re.sub('\s', '', line))
    return r_urls


def start():
    # 创建基础路径
    if not os.path.exists(path_base):
        os.makedirs(path_base)
        infos('创建字体保存路径成功！')
    # 在路径保存的前提下，读取url文件,遍历访问
    urls = find_all_urls()

    for url in urls:
        start_time = currDateFormate()
        infos('字体下载开始执行 START:', url, start_time)

        tel_types_main(url)

        end_time = currDateFormate()
        infos('字体下载执行结束 END  :', url, end_time)
        infos('字体下载共计耗时：', (end_time - start_time))
        infos('===================华丽的分割线===============================')


if __name__ == '__main__':
    check_url_isexist()

    start()
