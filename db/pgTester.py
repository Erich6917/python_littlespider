# -*- coding: utf-8 -*-
# @Time    : 2018/7/12 
# @Author  : ErichLee ErichLee@qq.com
# @File    : pgTester.py
# @Comment : 
#            

import sys
import db.PostgreSQLManage as pgManage
from util.logger_util import *

reload(sys)
sys.setdefaultencoding('utf-8')

pg_util = pgManage.Mysql()


def tel_inset():
    sql_execute = "insert into bloom_telnet(tel_key,tel_val) values('{}','{}')".format('storage', 'rabbit')
    infos("TEL 1 , Execute > {}".format(sql_execute))
    pg_util.insertOne(sql_execute)

    sql_select = "select count(1) from bloom_telnet where tel_key = '{}'".format('storage')
    rt = pg_util.getOne(sql_select)
    infos("TEL 2 , Execute > {}".format(sql_select))
    infos("        result > {}".format(rt))

    sql_delete = "delete from bloom_telnet where tel_key = '{}'".format('storage')
    pg_util.delete(sql_delete)
    infos("TEL 3 , Execute > {}".format(sql_select))


# tel_inset()

for j in range(1, 6, 2):
    print j