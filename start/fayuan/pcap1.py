# -*- coding: utf-8 -*-
# @Time    : 2019/4/13 
# @Author  : ErichLee ErichLee@qq.com
# @File    : pcap1.py
# @Comment : 
#            

import pcap
import dpkt
import time


def captData():
    pc = pcap.pcap()
    pc.setfilter('tcp port 80')
    for ptime, pdata in pc:
        anlyCap(ptime, pdata);


def anlyCap(ptime, pdata):
    content = "baidu.com";
    p = dpkt.ethernet.Ethernet(pdata)
    ipData = p.data
    if ipData.__class__.__name__ == 'IP':
        sip = '%d.%d.%d.%d' % tuple(map(ord, list(ipData.src)))
        dip = '%d.%d.%d.%d' % tuple(map(ord, list(ipData.dst)))
        tcpData = ipData.data

        appData = tcpData.data
        if appData.find(content) <> -1:
            print "find: " + content

        x = time.localtime(ptime)
        ptimeS = time.strftime('%Y-%m-%d %H:%M:%S', x)
        sport = tcpData.sport
        dport = tcpData.dport
        sportS = str(sport)
        dportS = str(dport)

        if tcpData.__class__.__name__ == 'TCP':
            if tcpData.dport == 80:  # HTTP
                print "========== " + ptimeS + " " + sip + ":" + sportS + " --> " + dip + ":" + dportS + " HTTP ==========";
                print appData
            elif tcpData.dport == 443:  # HTTPS
                print "========== " + ptimeS + " " + sip + ":" + sportS + " --> " + dip + ":" + dportS + " HTTPS ==========";
                print appData
            elif tcpData.dport == 25:  # SMTP
                print "========== " + ptimeS + " " + sip + ":" + sportS + " --> " + dip + ":" + dportS + " SMTP ==========";
                print appData
            else:
                print "========== " + ptimeS + " " + sip + ":" + sportS + " --> " + dip + ":" + dportS + " Other ==========";
                print appData
        elif tcpData.__class__.__name__ == 'UDP':
            print "========== " + ptimeS + " " + sip + ":" + sportS + " --> " + dip + ":" + dportS + " UDP ==========";
            print appData


captData()