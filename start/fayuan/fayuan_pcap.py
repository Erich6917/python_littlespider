# -*- coding: utf-8 -*-
# @Time    : 2019/4/4
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_video.py
# @Comment :
#

import pcap
import dpkt

host = 'host'
urlex = 'urlex'
pc = pcap.pcap()
pc.setfilter('tcp port 80')

for ptime, pdata in pc:
    host = ""
    urlex = ""
    p = dpkt.ethernet.Ethernet(pdata)
    if p.data.__class__.__name__ == 'IP':
        ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
        if p.data.data.__class__.__name__ == 'TCP':
            if p.data.data.dport == 80:
                # print p.data.data.data
                sStr1 = p.data.data.data
                # print "==============data=================="
                # print sStr1
                # print "===================================="
                sStr2 = 'Host: '
                sStr3 = 'Connection'
                sStr4 = 'GET /'
                sStr5 = ' HTTP/1.1'
                nPos = sStr1.find(sStr3)
                nPosa = sStr1.find(sStr5)
                if sStr1.find(sStr2) >= 0:
                    for n in range(sStr1.find(sStr2) + 6, nPos - 1):
                        host = sStr1[sStr1.find(sStr2) + 6:n]
                        # print "n:" + n.__str__() + " " + "host" + host
                if (sStr1.find(sStr4) >= 0):
                    for n in range(sStr1.find(sStr4) + 4, nPosa + 1):
                        urlex = sStr1[sStr1.find(sStr4) + 4:n]
                        # print "n:" + n.__str__() + " " + "urlex" + urlex
                result = host + urlex
                if result.__len__() > 0:
                    print "==============result=================="
                    print result
                    print "======================================"