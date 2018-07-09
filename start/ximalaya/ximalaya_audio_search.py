# -*- coding: utf-8 -*-
# @Time    : 2018/6/20
# @Author  : ErichLee ErichLee@qq.com
# @File    : spider_ximalaya2.py
# @Comment :
#
from ximalaya_audio import *

reload(sys)
sys.setdefaultencoding('utf-8')

# 查找URL

# 单个下载URL START
# start_find_category()

# 单个下载URL END
# ========================================================
# 批量下载URL START

# step1
# 下载首页所有需要下载目录
# start_find_cate_ids()

# re_msg = []
# re_msg.append(('你', '1'))
# re_msg.append(('你', '2'))
# re_msg.append(('我', '4'))
# re_msg.append(('他', '5'))

# infos('BEFORE > len[{}]'.format(len(re_msg)))
# sort_list = sorted(re_msg, key=lambda x: x[0], reverse=True)
# infos('AFTER > len[{}]'.format(len(sort_list)))


# step2 读取文件 ，依次下载
start_find_all_category()

# download_audio()
# 批量下载URL END
