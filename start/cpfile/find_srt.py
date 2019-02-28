# -*- coding: utf-8 -*-
# @Time    : 2018/9/27 
# @Author  : ErichLee ErichLee@qq.com
# @File    : find_srt.py
# @Comment : 
#            

import sys
import os, shutil
from util.file_check_util import *

reload(sys)
sys.setdefaultencoding('utf-8')


def find_srt_file():
    src = u'C:/Users/Administrator/Desktop/A字幕'
    file_list = get_all_files_path_name(src)
    for each in file_list:
        file_name, file_path = each[0], each[1]
        if file_name.endswith('.简体.srt'):
            try:
                shutil.copyfile(file_path, u'target/{}'.format(file_name))
            except:
                print file_name, file_path


find_srt_file()
