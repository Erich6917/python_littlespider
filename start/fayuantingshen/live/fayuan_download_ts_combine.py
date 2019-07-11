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


def get_curr_dir_names(path_source='.'):
    rt_dirs = []
    for filename in os.listdir(path_source):
        # path = os.path.join(path_source, filename)
        path = '{}/{}'.format(path_source,filename)
        if os.path.isdir(path):
            rt_dirs.append((filename, path))
    return rt_dirs


def get_all_files_path_name(path_source='.'):
    file_list = []
    for root, dirs, files in os.walk(path_source):
        for filename in files:
            file_msg = filename, os.path.join(root, filename), root
            file_list.append(file_msg)
    return file_list


def merge_file(path, new_name):
    os.chdir(path)
    cmd = "copy /b * new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "{}.mp4".format(new_name))


def merge_files(path, new_name):
    os.chdir(path)
    cmd = "copy /b *.ts new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    if os.path.isfile("new.tmp"):
        os.rename("new.tmp", "{}.mp4".format(new_name))


def start_merge():
    curr = os.getcwd()

    source = 'C:/Users/Administrator/Desktop/fayuan/source/download/minshi/beijing/el-nee'
    file_list = get_curr_dir_names(source)

    for name, path in file_list:
        print path, name
        os.chdir(curr)
        merge_files(path, name)
        # print source,name


if __name__ == '__main__':
    start_merge()
