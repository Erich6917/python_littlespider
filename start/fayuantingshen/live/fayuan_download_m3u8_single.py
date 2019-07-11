# -*- coding: utf-8 -*-
# @Time    : 2019/4/20 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_download_m3u8.py
# @Comment : 
#            

import os
import sys
import requests
import datetime
from Crypto.Cipher import AES
# from binascii import b2a_hex, a2b_hex
# import util.file_check_util as file_util

reload(sys)
sys.setdefaultencoding('utf-8')


def get_all_files_path_name_endswith(path_source, ends):
    # file_util.get_all_files()
    file_list = []
    for root, dirs, files in os.walk(path_source):
        for filename in files:
            if filename.endswith(ends):
                file_msg = filename, os.path.join(root, filename), root
                file_list.append(file_msg)
    return file_list


def download(url, source_path, new_name):
    # 新建日期文件夹
    download_path = os.path.join(source_path, new_name)
    # print download_path
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    all_content = requests.get(url).text  # 获取第一层M3U8文件内容
    if "#EXTM3U" not in all_content:
        # raise BaseException("非M3U8的链接")
        print ("非M3U8的链接")
        return

    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line  # 拼出第二层m3u8的URL
                url =url.strip('\r').strip('\n')
                all_content = requests.get(url).text
                break

    file_line = all_content.split("\n")

    unknow = True
    key = ""
    for index, line in enumerate(file_line):  # 第二层
        if "#EXT-X-KEY" in line:  # 找解密Key
            method_pos = line.find("METHOD")
            comma_pos = line.find(",")
            method = line[method_pos:comma_pos].split('=')[1]
            print "Decode Method：", method

            uri_pos = line.find("URI")
            quotation_mark_pos = line.rfind('"')
            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

            key_url = url.rsplit("/", 1)[0] + "/" + key_path  # 拼出key解密密钥URL
            res = requests.get(key_url)
            key = res.content
            print "key：", key

        if "EXTINF" in line:  # 找ts地址并下载
            unknow = False
            pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]  # 拼出ts片段的URL
            # print pd_url
            pd_url = pd_url.strip('\r').strip('\n')

            c_fule_name = file_line[index + 1].rsplit("/", 1)[-1]
            c_fule_name = c_fule_name.replace('\r', '')
            res = requests.get(pd_url)
            #
            if len(key):  # AES 解密
                cryptor = AES.new(key, AES.MODE_CBC, key)
                with open(os.path.join(download_path, c_fule_name + ".mp4"), 'ab') as f:
                    f.write(cryptor.decrypt(res.content))
            else:
                # print os.path.join(download_path, c_fule_name)
                with open(os.path.join(download_path, c_fule_name), 'ab') as f:
                    f.write(res.content)
                    f.flush()
    if unknow:
        # raise BaseException("未找到对应的下载链接")
        print("未找到对应的下载链接")
        return
    else:
        # merge_file(download_path, new_name)
        print u"下载完成"
        return u'success!'


def merge_file(path, new_name):
    os.chdir(path)
    cmd = "copy /b * new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "{}.mp4".format(new_name))


def start_download():
    file_list = get_all_files_path_name_endswith('source/zone', '.txt')
    # source_path = os.path.join(os.getcwd(), 'download')
    curr = os.getcwd()
    file_log = open('logger.log', 'a+')
    for file_name, file_path, file_root in file_list:
        # print file_name, file_path, file_root
        output_root = file_root.replace('/zone', '/download')
        rt_list = open(file_path).readlines()
        for zone_info in rt_list:
            each = zone_info.replace('\n', '').split('\t')
            href, name = each[0], each[1]
            print 'downloading', href, name

            # os.chdir(curr)
            try:
                if download(href, output_root, name):
                    file_log.write('success\t{}'.format(each))
                else:
                    file_log.write('failed \t{}'.format(each))
            except Exception as e:
                file_log.write('error\t{}\t{}'.format(each, e))
                print e


if __name__ == '__main__':
    # start_download()
    # url = u'http://live5.bjcourt.gov.cn:8080/edge/defaults/201904/18/defaults/121349_646/KANP_0.vod.m3u\r\n'
    # print url.strip('\r').strip('\n')
    # print 'a'
    # url = "http://live5.bjc
    # ourt.gov.cn:8080/edge/defaults/201904/18/defaults/102954_431/24AG_0.vod.m3u8"
    url = 'http://live3.bjcourt.gov.cn:8080/edge/defaults/201904/17/defaults/140457_069/vod_ca_9.menu.m3u8'
    download(url,'test','down')

    # merge_file(u'C:/Personal/workspace/mygit_py2/littlespider/start/fayuantingshen/live/download/20190422_143120')
