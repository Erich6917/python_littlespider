# -*- coding: utf-8 -*-
# @Time    : 2017/12/10 
# @Author  : LIYUAN134
# @File    : newsEntity.py
# @Commment: pa_voice_news 实体类
#


class pa_voice_news(object):
    @property
    def news_title(self):
        return self._news_title

    @news_title.setter
    def news_title(self, value):
        self._news_title = value

    @property
    def news_url(self):
        return self._news_url

    @news_url.setter
    def news_url(self, value):
        self._news_url = value

    @property
    def news_scope(self):
        return self._news_scope

    @news_scope.setter
    def news_scope(self, value):
        self._news_scope = value

    @property
    def news_realdate(self):
        return self._news_realdate

    @news_realdate.setter
    def news_realdate(self, value):
        self._news_realdate = value

    @property
    def news_message(self):
        return self._news_message

    @news_message.setter
    def news_message(self, value):
        self._news_message = value


# def test_entity():
#     news = pa_voice_news()
#
#     news.news_url = 'http://sina'
#     news.news_scope = 'scope'
#     news.news_title = 'title'
#     news.news_message = 'message'
#
#     print news.news_title, news.news_url, news.news_scope, news.news_message
