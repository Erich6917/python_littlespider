# -*- coding: utf-8 -*-
# @Time    : 2018/1/15
# @Author  : LIYUAN134
# @File    : MongoManage.py
# @Commment:
#
from pymongo import MongoClient

port = 27017
# 建立数据库连接
client = MongoClient('localhost', port)
# 连接目标数据库
db = client.jade

cursor = db.col.find()

for doc in cursor:
    print doc['title']
