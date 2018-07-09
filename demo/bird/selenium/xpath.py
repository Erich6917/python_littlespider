# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 
# @Author  : LIYUAN134
# @File    : xpath.py
# @Commment: 
#
import sys

import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import time
import random
from lxml import etree

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

reload(sys)
sys.setdefaultencoding('UTF-8')

cookie = 'TYCID=b9042fd0fbf811e7ad821b31dcb048ff; undefined=b9042fd0fbf811e7ad821b31dcb048ff; ssuid=1244323428; jsid=SEM-BAIDU-CG-SY-000402; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODc1MTg0NTE4OSIsImlhdCI6MTUxNjU5MzA0OCwiZXhwIjoxNTMyMTQ1MDQ4fQ.XfowIdLycJr-QCgOBh2--UTsscFOsMRv7qOxB4-pPKFc7VlBlkPkmZ5NiCdV48TwAQFNHDirmHB1DzWNkuUMJQ%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218751845189%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODc1MTg0NTE4OSIsImlhdCI6MTUxNjU5MzA0OCwiZXhwIjoxNTMyMTQ1MDQ4fQ.XfowIdLycJr-QCgOBh2--UTsscFOsMRv7qOxB4-pPKFc7VlBlkPkmZ5NiCdV48TwAQFNHDirmHB1DzWNkuUMJQ; RTYCID=1487b6741aed4ce3a940cff05b047fc9; aliyungf_tc=AQAAAOwUYw2DMwUATTM/tyOkpcrO4XJe; csrfToken=QI1h0xSOM26Tj07yE5s34-e_; _csrf=5mtFDIcwEORrMrefbdecfA==; OA=7mf2rRDs/f3WEAt0+D9n0bdC7+I30ioMZ3pYTJTqdY8MPBfbmjEwQEJikDzjSHoh; _csrf_bk=50bcb5774373cfc32253d60bad18ed27; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1516324904,1516593017,1516691667,1516849381; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1516868356'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome' \
                         '/61.0.3163.79 Safari/537.36', 'Cookie': cookie}


def tel_url(urls):
    print urls

    s = requests.Session()
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    res = s.get(urls, verify=False, headers=headers)
    rtmsg = res.text
    html = etree.HTML(rtmsg)
    # print rtmsg
    if rtmsg:
        # a_list = html.xpath("//span[@id='web-content']/div/div/div/div/div/div/div/div/a")

        a_list = html.xpath("//*[@id='web-content']/div/div/div/div/div/div/div/div/a/span")
        for tt in a_list:
            print tt
    else:
        print '页面解析失败'

if __name__ == '__main__':
    url = 'https://nanjing.tianyancha.com/search'
    url = 'https://nanjing.tianyancha.com/search/ocD'
    tel_url(url)
