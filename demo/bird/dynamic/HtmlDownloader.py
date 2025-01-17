# -*- coding: utf-8 -*-
# @Time    : 2018/2/5 
# @Author  : LIYUAN134
# @File    : HtmlDownloader.py
# @Commment: 
#            
import requests


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
