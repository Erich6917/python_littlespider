# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 
# @Author  : LIYUAN134
# @File    : demo.py
# @Commment: 
#            
import requests
import urllib2

# import socket
# socket.getaddrinfo('127.0.0.1', 8080)
# true_socket = socket.socket
#
# ipbind = '11.240.138.214'
# ipbind = '127.0.0.1'
#
#
# def bound_socket(*a, **k):
#     sock = true_socket(*a, **k)
#     sock.bind((ipbind, 0))
#     return sock
#
#
# socket.socket = bound_socket

BASEURL = 'http://news.sina.news.cn/'
# BASEURL = 'https://trac.edgewall.org/ticket/8657'
# res = requests.get(BASEURL)


response = urllib2.urlopen(BASEURL)
data = response.read()
print data

