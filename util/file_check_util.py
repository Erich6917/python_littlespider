# -*- coding: utf-8 -*-
# @Time    : 2018/6/4 
# @Author  : ErichLee ErichLee@qq.com
# @File    : file_check_util.py
# @Comment : IO流检查
#            

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')


# def current_path():
#     """
#         获取当前文件路径
#         兼容pycharm和cmd直接运行脚本路径
#     """
#     if getattr(sys, 'frozen', False):
#         apply_path = os.path.dirname(sys.executable)
#     elif __file__:
#         apply_path = os.path.dirname(__file__)
#     return apply_path


def get_all_dirs(path_source='.'):
    dir_list = []
    for root, dirs, files in os.walk(path_source):
        for c_dir in dirs:
            dir_list.append(c_dir)
    return dir_list


def get_all_files(path_source='.'):
    file_list = []
    for root, dirs, files in os.walk(path_source):
        for filename in files:
            file_list.append(filename)
    return file_list
