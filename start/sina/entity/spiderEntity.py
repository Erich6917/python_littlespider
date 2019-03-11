# -*- coding: utf-8 -*-
# @Time    : 2017/12/10 
# @Author  : LIYUAN134
# @File    : newsEntity.py
# @Commment: 爬虫通用实体类
#


class spiderEntity(object):
    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, value):
        self._scope = value
