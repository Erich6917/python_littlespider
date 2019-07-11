# -*- coding: utf-8 -*-
# @Time    : 2018/9/25 
# @Author  : ErichLee ErichLee@qq.com
# @File    : start.py
# @Comment : 
#
import re
import sys

import os

reload(sys)
sys.setdefaultencoding('utf-8')


def start():
    path = 'source'
    target = 'target'
    file_list = get_all_files_path_name(path)

    if not file_list:
        raise Exception('Not Found SOURCE！')
    if not os.path.exists(target):
        os.mkdir(target)

    sample = get_sample()

    for file in file_list:
        file_name, file_path = file[0], file[1]
        if file_name.endswith('wav'):
            file_name = re.sub('\\..*', '', file_name)
            file_name = '{}/{}.txt'.format(target, file_name)
            with open(file_name, 'w') as writer:
                writer.writelines(sample)


def get_sample():
    try:
        with open('sample.txt', 'r') as file:
            return file.readlines()
    except:
        raise Exception('Not Found sample.txt')


def get_all_files_path_name(path_source='.'):
    file_list = []
    for root, dirs, files in os.walk(path_source):
        for filename in files:
            file_msg = filename, os.path.join(root, filename), root
            file_list.append(file_msg)
    return file_list


start()