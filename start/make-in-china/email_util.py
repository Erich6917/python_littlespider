# -*- coding: utf-8 -*-
# @Time    : 2018/1/31 
# @Author  : LIYUAN134
# @File    : my_email.py
# @Commment: 
#
from email.header import Header
from email.mime.text import MIMEText

from email.utils import parseaddr, formataddr

import smtplib


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(msg):
    from_addr = '18751845189@163.com'
    from_password = '@MICzdl37wznb123'

    to_addr = 'newbaiha@163.com'
    smtp_server = 'smtp.163.com'
    message = u'一个亿小目标发送邮件功能测试 \n' + str(msg)
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'雷锋<%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员<%s>' % to_addr)
    msg['Subject'] = Header(u'重新登录')

    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, from_password)
    server.sendmail(from_addr, [to_addr], msg.as_string())

    server.quit()


