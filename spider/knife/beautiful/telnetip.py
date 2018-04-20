# -*- coding: utf-8 -*-
# @Time    : 2017/12/15 
# @Author  : LIYUAN134
# @File    : telnetip.py
# @Commment: 
#            

import urllib2
import re
from bs4 import BeautifulSoup


# url = 'http://www.xicidaili.com/nn/1'
def _findIps():
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent

    url = 'http://www.xicidaili.com/nn/1'
    req = urllib2.Request(url, headers=header)
    res = urllib2.urlopen(req).read()

    soup = BeautifulSoup(res, 'html5lib')
    ips = soup.findAll('tr')
    f = open("src/proxy.text", "w")
    # print ips
    #
    for x in range(1, len(ips)):
        ip = ips[x]
        tds = ip.findAll("td")
        ip = tds[1].text
        port = tds[2].text
        print 'ip:', ip, 'port', port
        host = ip + ':' + port
        f.write(host)
        f.write('\n')


# _findIps()


def test_ping():
    import urllib
    import socket
    socket.setdefaulttimeout(3)
    f = open("src/proxy.text")
    fresh = open("src/fresh.text", "w")
    lines = f.readlines()
    proxys = []
    # for i in range(0, len(lines))
    print len(lines)
    for host in lines:
        host = re.sub('\s', '', host)
        proxy_host = "http://" + host
        proxy_temp = {"http": proxy_host}
        proxys.append(proxy_temp)
    url = "http://ip.chinaz.com/getip.aspx"
    count = 0
    for proxy in proxys:



        try:
            count += 1
            print 'ping ... ', proxy,
            res = urllib.urlopen(url, proxies=proxy).read()
            # print res
            print res
            fresh.write(proxy['http'])
            # print 'SUCCESS'
        except Exception, e:
            # print proxy
            # continue
            print 'ERROR',
            print e
        else:
            if fresh:
                fresh.close()
    print


test_ping()
