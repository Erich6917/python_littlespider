# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 
# @Author  : ErichLee ErichLee@qq.com
# @File    : ximalaya_global_map.py
# @Comment : 喜马拉雅相关全局变量
#            

import sys
import json
from util.loggerUtil import *

reload(sys)
sys.setdefaultencoding('utf-8')


class GlobalMap:
    map = {}

    def __init__(self):
        self.set_map('', '')
        self.set_map('', '')
        self.set_map('', '')

    # 拼装成字典构造全局变量  借鉴map  包含变量的增删改查


    def set_map(self, key, value):
        if (isinstance(value, dict)):
            value = json.dumps(value)
        self.map[key] = value

    def set(self, **keys):
        try:
            for key_, value_ in keys.items():
                self.map[key_] = str(value_)
                infos(key_ + ":" + str(value_))
        except BaseException as msg:
            errors(msg)
            raise msg

    def del_map(self, key):
        try:
            del self.map[key]
            return self.map
        except KeyError:
            errors("key:'" + str(key) + "'  不存在")

    def get(self, *args):
        try:
            dic = {}
            for key in args:
                if len(args) == 1:
                    dic = self.map[key]
                    infos(key + ":" + str(dic))
                elif len(args) == 1 and args[0] == 'all':
                    dic = self.map
                else:
                    dic[key] = self.map[key]
            return dic
        except KeyError:
            infos("key:'" + str(key) + "'  不存在")
            return 'Null_'
