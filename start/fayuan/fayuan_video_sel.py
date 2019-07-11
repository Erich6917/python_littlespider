# -*- coding: utf-8 -*-
# @Time    : 2019/4/4 
# @Author  : ErichLee ErichLee@qq.com
# @File    : fayuan_video.py
# @Comment : 
#
import re
import sys
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf-8')

hd_jump2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'player.videoincloud.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    # 'Cookie': "_uab_collina=155435660766304150643617; acw_tc=76b20ff015543566239131760e6732ac0abb80b6a036506c7f5ec4e8c6b492; _uab_collina=155435665378754705870108; Hm_lvt_2e0edde4e3669a50ace26a2cddb33e60=1555061563; acw_sc__v3=5cb1ffeface93411573e9202ba34a1bfc4198683; acw_sc__v2=5cb2008c4805ddca6a19e618caa81447b5c445ca; _pk_ref.1.a5e3=%5B%22%22%2C%22%22%2C1555169417%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DSHaaIG5JZTKm02HKF2N_TpAKJDfFesWNDPeYJknWwEgyMPW8nDAd57dmbV0VyzqtmkPaNuJ3RlUoRkYzDFiqE_%26wd%3D%26eqid%3Da97c287800007118000000055ca5998d%22%5D; _pk_ses.1.a5e3=*; _pk_id.1.a5e3=3d60bc686bb0d63d.1554356608.8.1555170714.1555169417.; SERVERID=2666959f4331fe3ad439f4610ea751e3|1555170720|1555165944"

}




def search_real_url(url):
    # url = 'http://player.videoincloud.com/vod/3242311?src=gkw&cc=1'

    driver = webdriver.Chrome()
    driver.set_page_load_timeout(20)
    driver.get(url)

    matcher = re.findall('src:\'(.+\.mp4)', res.text)
    if matcher:
        return str(matcher[0])
        # else:
        #     print 'not match', url
        #     print res.text


def file_combine():
    file_target = open('url_telnet.txt', 'a+')

    with open('detail_minshi.txt', 'r+') as file_detail:
        lines = file_detail.readlines()
        for line in lines:
            arr_line = line.split('\t')
            video_id = arr_line[0]
            url = 'http://tingshen.court.gov.cn/live/{}\n'.format(video_id)
            file_target.write(url)


# start_download()
# url = 'http://tingshen.court.gov.cn/live/5195910'
# print search_jump_url(url)
# url = 'http://player.videoincloud.com/vod/3246052?src=gkw&cc=1'


def start_downlaod_local():
    file_mp4 = open('source_mp4.txt', 'a+')
    file_error_mp4 = open('error_mp4.txt', 'a+')
    with open('url_source.txt', 'a+') as file_source:
        lines = file_source.readlines()
        for line in lines:
            arr_line = line.replace('\n', '').split('\t')
            source_url, target_url = arr_line[0], arr_line[1]
            # print source_url, target_url
            source_mp4 = search_real_url(target_url)
            if not source_mp4:
                file_error_mp4.write(line)
                print 'error', target_url
            else:
                rt_msg = '{}\t{}\t{}\n'.format(source_url, target_url, source_mp4)
                file_mp4.write(rt_msg)
                print rt_msg

target_url = 'http://player.videoincloud.com/vod/3080304?src=gkw&cc=1'
print search_real_url(target_url)
# file_combine()
