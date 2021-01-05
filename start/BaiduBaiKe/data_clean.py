# -*- coding: utf-8 -*-
# @Time    : 2019/8/19 
# @Author  : ErichLee ErichLee@qq.com
# @File    : data_clean.py
# @Comment : 
#            

import sys

import os

reload(sys)
sys.setdefaultencoding('utf-8')

f_name = u'qa-newWOrd'


# 两个文本比较
def start_compare():
    file_path_source = u'source/clean/{}.txt'.format(f_name)
    file_path_succ = u'source/clean/{}-succ.txt'.format(f_name)

    file_path_out = u'source/clean/{}_failed.txt'.format(f_name)

    lines_source = open(file_path_source, 'r').readlines()
    lines_succ = open(file_path_succ, 'r').readlines()

    file_out = open(file_path_out, 'w+')

    print len(lines_source), len(lines_succ)

    list_succ = []
    for line in lines_succ:
        line_arr = line.split('\t')
        list_succ.append(line_arr[0])
    counter = 0

    write_msg = []
    for line in lines_source:
        counter += 1

        key = line.strip().split(' ')
        if len(key) == 5:
            name = key[0]
            if name in list_succ:
                list_succ.remove(name)
            else:
                write_msg.append(line)
        else:
            print line
        if counter % 500 == 0:
            print counter, len(lines_source), len(list_succ)
            file_out.writelines(''.join(write_msg))
            file_out.flush()
            write_msg = []
    if write_msg:
        file_out.writelines(''.join(write_msg))
        file_out.flush()
        file_out.close()


def start_parse_succ():
    path = u'source/clean'
    lines = open(os.path.join(path, u'{}-succ.txt'.format(f_name)), 'r').readlines()
    print len(lines)

    file_succ = open(os.path.join(path, '{}_succ.txt'.format(f_name)), 'w+')
    file_no_good = open(os.path.join(path, '{}_no_like.txt'.format(f_name)), 'w+')
    file_no_tag = open(os.path.join(path, '{}_no_tag.txt'.format(f_name)), 'w+')

    rt_succ = []
    rt_no_good = []
    rt_no_flag = []
    for line in lines:
        arr = line.split('\t')
        if len(arr) != 4:
            # print line
            rt_no_good.append(line)
            continue
        name, times, like, tag = arr[0], arr[1], arr[2], arr[3].strip()
        # flag_good = (goods or goods != 'None')
        # flag_tag=
        if (like and like != u'None'):
            if tag:
                rt_succ.append(line)
            else:
                rt_no_flag.append(line)
        else:
            rt_no_good.append(line)

    file_succ.writelines(''.join(rt_succ))
    file_no_good.writelines(''.join(rt_no_good))
    file_no_tag.writelines(''.join(rt_no_flag))


def start_check():
    file_path_source = u'source/clean/{}.txt'.format(f_name)
    file_path_succ = u'source/clean/{}-succ.txt'.format(f_name)

    file_path_out = u'source/clean/out.txt'

    # lines_source = open(file_path_source, 'r').readlines()
    lines_succ = open(file_path_succ, 'r').readlines()

    # list_msg=[]
    # for line in lines_succ:
    #     line_arr = line.strip().split('\t')
    #     list_msg.append(line_arr[0])
    # print len(lines_succ),len(list_msg), len(set(list_msg))
    #
    # if True:
    #     return


    # list_succ = []
    # list_source = []
    file_out = open(u'source/clean/succ.txt', 'w')
    counter = 0
    list_out = []
    out_msg = []
    for line in lines_succ:
        counter += 1
        line_arr = line.split('\t')
        name = line_arr[0]
        if name in list_out:
            print name
        else:
            list_out.append(line_arr[0])
            out_msg.append(line)
            if counter % 1000 == 0:
                print 'flush', counter
                file_out.writelines(''.join(out_msg))
                file_out.flush()
                out_msg = []

    if out_msg:
        file_out.writelines(''.join(out_msg))

    file_out.flush()
    file_out.close()

# start_check()
# start_compare()
# start_parse_succ()
