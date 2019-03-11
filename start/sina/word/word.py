# -*- coding: utf-8 -*-
# @Time    : 2018/2/8 
# @Author  : LIYUAN134
# @File    : word.py
# @Commment: 
#            
from dbutil.DBNewsUtil import DBNews
from dateCheckUtil import *
from EmailSendUtil import send_emails
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')

dbnews = DBNews()


def start():
    end =   700001
    start = 640001
    steps = 5000
    try:
        files = open(u'财经素材10万007.txt', 'a')
        while start <= end - steps:
            # end = start + steps
            print start, start + steps
            print '数据获取中...', currDateFormate()
            rt = dbnews.get_finance_limts(steps, start)
            start += steps
            print '数据获取完毕，保存中...', currDateFormate()
            for msg in rt:
                # print msg[0]
                files.write(str(msg[0]) + '\n')
    except Exception, e:
        print 'ERROR', e
    finally:
        files.close()


if __name__ == '__main__':
    start()
    send_emails(u'单位名称数据下载任务完成!')