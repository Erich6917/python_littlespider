# -*- coding: utf-8 -*-
# @Time    : 2020-12-16 
# @Author  : ErichLee ErichLee@qq.com
# @File    : parseUtil.py
# @Comment : 
#            

import sys
from util.file_check_util import *

reload(sys)
sys.setdefaultencoding('utf-8')


def parse_city():
    file_company = open('a.txt', 'r')
    for line in file_company:
        city = line.split(":")[0]
        print "\"{}\",".format(city.lower()),


def file_combine():
    file = open("AnHui_phone.txt", 'a')

    file_list = get_all_files_path_name("file")
    for name, path, root in file_list:
        print name, path, root
        # file_target = open('anhui_phone.txt', 'a+')
        lines = open(path, 'r').readlines()
        for line in lines:
            file.write(line)
            file.flush()

        # with open('detail_minshi.txt', 'r+') as file_detail:
        #     lines = file_detail.readlines()
        #     for line in lines:
        #         arr_line = line.split('\t')
        #         video_id = arr_line[0]
        #         url = 'http://tingshen.court.gov.cn/live/{}\n'.format(video_id)
        #         file_target.write(url)
        # parse_city()
file_combine()