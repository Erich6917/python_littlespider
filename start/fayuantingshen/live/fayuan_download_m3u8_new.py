# -*- coding: utf-8 -*-
# @Time    : 2019/4/20 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_download_m3u8.py
# @Comment : 
#            

import os
import sys
import time
import requests
import datetime
from Crypto.Cipher import AES

import socket

timeout = 5
socket.setdefaulttimeout(timeout)
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
    all_content = requests.get(url).text  # 获取第一层M3U8文件内容
    if "#EXTM3U" not in all_content:
        # raise BaseException("非M3U8的链接")
        print (u"非M3U8的链接")
        return
    # 新建日期文件夹
    download_path = os.path.join(source_path, new_name)
    # print download_path
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line  # 拼出第二层m3u8的URL
                url = url.strip('\r').strip('\n')
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


def save_download_url(url, source_path, new_name):
    all_content = requests.get(url).text  # 获取第一层M3U8文件内容
    if "#EXTM3U" not in all_content:
        # raise BaseException("非M3U8的链接")
        print (u"非M3U8的链接")
        return
    # 新建日期文件夹
    download_path = os.path.join(source_path, new_name)
    # print download_path
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    if "EXT-X-STREAM-INF" in all_content:  # 第一层
        file_line = all_content.split("\n")
        for line in file_line:
            if '.m3u8' in line:
                url = url.rsplit("/", 1)[0] + "/" + line  # 拼出第二层m3u8的URL
                url = url.strip('\r').strip('\n')
                all_content = requests.get(url).text
                break

    file_line = all_content.split("\n")

    unknow = True
    key = ""

    rt_list = []
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

            rt_msg = '{}\t{}'.format(c_fule_name, pd_url)
            rt_list.append(rt_msg)

            if True:
                continue
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
        return rt_list


def merge_file(path, new_name):
    os.chdir(path)
    cmd = "copy /b * new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "{}.mp4".format(new_name))


def start_download_address():
    file_list = get_all_files_path_name_endswith('source/zone', '.txt')
    # source_path = os.path.join(os.getcwd(), 'download')
    # curr = os.getcwd()
    file_log = open('logger.log', 'a+')
    for file_name, file_path, file_root in file_list:
        print file_name, file_path, file_root

        output_root = file_root.replace('/zone', '/download-address')
        rt_list = open(file_path).readlines()
        for zone_info in rt_list:
            each = zone_info.replace('\n', '').split('\t')
            href, title = each[0], each[1]
            print 'downloading', href, title

            # os.chdir(curr)
            try:
                rt_list = save_download_url(href, output_root, title)

                if rt_list is None:
                    print 'Not Found Download Url'
                    return
                dict_url = {}

                # 去重
                for msg_each in rt_list:
                    each = msg_each.strip().split('\t')
                    name, url = each[0], each[1]
                    # print name, url
                    dict_url.update({name: url})
                if len(dict_url) > 0:
                    # 生成对应下载地址文本
                    print 'saving ... {}'.format(len(dict_url))

                    rt_msg = ['{}\t{}'.format(key, val) for key, val in dict_url.items()]
                    with open(os.path.join(output_root, title, '{}.txt'.format(title)), 'a+') as file_download:
                        file_download.writelines("\n".join(rt_msg))
                else:
                    print 'empty'
            except Exception as e:
                file_log.write('error\t{}\t{}'.format(each, e))
                print e


def download_ts(href):
    # 文件下载 ，超时设置
    try:
        res = requests.get(href)
        return res.content
    except Exception as e:
        print 'Error', e


def start_download_mp4():
    file_list = get_all_files_path_name_endswith('source/download-address', '.txt')
    # source_path = os.path.join(os.getcwd(), 'download')
    # curr = os.getcwd()
    file_log = open('logger.log', 'a+')
    for file_name, file_path, file_root in file_list:
        print file_name, file_path, file_root

        output_root = file_root.replace('/download-address', '/download')
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        rt_list = open(file_path).readlines()
        for zone_info in rt_list:
            each = zone_info.strip().split('\t')
            title, href = each[0], each[1]
            # print 'downloading', href, title
            content = download_ts(href)
            if content:
                # print 'writing', output_root, title
                with open(os.path.join(output_root, title), 'ab') as f:
                    f.write(content)
                    f.flush()
            else:
                print 'ERROR', href


def start_download_gogogo():
    curr_time = str(time.strftime("%Y%m%d%H%M", time.localtime()))
    logger_name = 'logger_down_{}.log'.format(curr_time)
    logger = open(logger_name, 'a+')
    logger.writelines('================START===========================\n')

    try:
        file_list = get_all_files_path_name_endswith('source/download-address', '.txt')
        msg_first = u'================本次执行任务个数:{}\n'.format(len(file_list))
        logger.write(msg_first)

        # source_path = os.path.join(os.getcwd(), 'download')
        # curr = os.getcwd()

        for index in range(0, len(file_list)):
            file_name, file_path, file_root = file_list[index]
            # print index, file_name, file_path, file_root
            msg_start = u'START\t{}\t{}\n'.format(index, file_name)
            logger.write(msg_start)
            logger.flush()

            output_root = file_root.replace('/download-address', '/download')
            if not os.path.exists(output_root):
                os.makedirs(output_root)
            # download each file
            rt_list = open(file_path).readlines()
            for zone_info in rt_list:
                each = zone_info.strip().split('\t')
                title, href = each[0], each[1]
                # print 'downloading', href, title
                content = download_ts(href)
                if content:
                    # print 'writing', output_root, title
                    with open(os.path.join(output_root, title), 'ab') as f:
                        f.write(content)
                else:
                    msg_err = 'ERROR\t{}\t{}\n'.format(file_name, href)
                    logger.write(msg_err)
                    logger.flush()
                    # print 'ERROR', href
            msg_end = 'END\t{}\t{}\n'.format(index, file_name)
            logger.write(msg_end)
            logger.flush()

    except Exception as e:
        logger.write('ERROR {}'.format(e))
    finally:
        logger.close()
        #
        # file_list = get_all_files_path_name_endswith('source/download-address', '.txt')
        # source_path = os.path.join(os.getcwd(), 'download')
        # curr = os.getcwd()
        # for file_name, file_path, file_root in file_list:
        #     print file_name, file_path, file_root
        #
        #     output_root = file_root.replace('/download-address', '/download')
        #     if not os.path.exists(output_root):
        #         os.makedirs(output_root)
        #
        #     rt_list = open(file_path).readlines()
        #     for zone_info in rt_list:
        #         each = zone_info.strip().split('\t')
        #         title, href = each[0], each[1]
        #         # print 'downloading', href, title
        #         content = download_ts(href)
        #         if content:
        #             # print 'writing', output_root, title
        #             with open(os.path.join(output_root, title), 'ab') as f:
        #                 f.write(content)
        #                 f.flush()
        #         else:
        #             print 'ERROR',href


def start_download_url():
    dict_url = {}

    url = 'source/zone/download_url.txt'
    msg_lines = open(url, 'r').readlines()
    for msg_each in msg_lines:
        each = msg_each.strip().split('\t')
        name, url = each[0], each[1]
        print name, url
        dict_url.update({name: url})
        # res = requests.get(url)
    #     if res:
    #         with open(os.path.join('source/zone/332211446655', '{}.mp4'.format(name)), 'ab') as f:
    #             f.write(res.content)
    #             f.flush()


    print 'list', len(msg_lines)
    print 'dict', len(dict_url.items())

    # for key, val in dict_url.items():
    #     print key, val


if __name__ == '__main__':
    # start_download_address()

    # start_download_mp4()

    start_download_gogogo()


    # start_download_url()

    # url = u'http://live5.bjcourt.gov.cn:8080/edge/defaults/201904/18/defaults/121349_646/KANP_0.vod.m3u\r\n'
    # print url.strip('\r').strip('\n')
    # print 'a'
    # url = "http://live5.bjcourt.gov.cn:8080/edge/defaults/201904/17/defaults/091537_328/6DD2_0.vod.m3u8"
    # download(url, 'source/test', '111')

    # merge_file(u'C:/Personal/workspace/mygit_py2/littlespider/start/fayuantingshen/live/download/20190422_143120'
