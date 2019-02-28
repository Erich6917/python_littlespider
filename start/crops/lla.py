# -*- coding: utf-8 -*-
# @Time    : 2018/11/14
# @Author  : ErichLee ErichLee@qq.com
# @File    : lla.py
# @Comment :
#

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

arr = [1, 2, 3, 4, 5, 6]
ss = filter(lambda x: x>5, range(1, 10))
print ss

print map(lambda x: x > 2, [1, 2, 3, 4, 5])
