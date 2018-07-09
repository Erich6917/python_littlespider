# -*- coding: utf-8 -*-
# @Time    : 2018/6/20
# @Author  : ErichLee ErichLee@qq.com
# @File    : ximalaya_audio.py
# @Comment :
#
import re

from bs4 import BeautifulSoup

import ximalaya_soup as soup
from util.DateCheckUtil import *
from util.file_check_util import *
from util.logger_util import *

reload(sys)
sys.setdefaultencoding('utf-8')
hd = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Host': 'www.ximalaya.com'
}

glb_path_source = u'source'
glb_path_save_urls = os.path.join(glb_path_source, 'urls')
glb_path_save_parse = os.path.join(glb_path_source, 'url')
glb_path_save_audio = os.path.join(glb_path_source, 'audio')
glb_path_save_config = os.path.join(glb_path_source, 'config')


def init_path():
    global glb_path_source, glb_path_save_urls, glb_path_save_audio
    if not os.path.exists(glb_path_source):
        infos("make dir source")
        os.mkdir(glb_path_source)
    if not os.path.exists(glb_path_save_urls):
        infos('make dir path_save_url')
        os.mkdir(glb_path_save_urls)
    if not os.path.exists(glb_path_save_audio):
        infos('make dir path_save_audio')
        os.mkdir(glb_path_save_audio)


def get_talking_list(tel_url):
    # url = 'http://www.ximalaya.com/yingshi/11438377/'
    # url = 'http://www.ximalaya.com/yingshi/8284644/'

    try:
        msg_all = soup.request_headers(tel_url, headers=hd)
    except Exception, e:
        infos('Telnet 报错 URL > {}'.format(tel_url))
        return

    rt_list_tuple = []

    reg_clean_s1 = 'title=\"([^"]+)\"\s*href=\"([^"]+)\"'
    reg_second_level = r'/?[^/]+/[^/]+/.+'
    msg_clean_s1 = re.findall(reg_clean_s1, msg_all)
    if msg_clean_s1:
        for each in msg_clean_s1:
            tar_url = re.search(reg_second_level, each[1])
            if tar_url:
                rt_info = (each[0], each[1])
                # print '成功发现目录,', rt_info
                rt_list_tuple.append(rt_info)
                # else:
                #     print '不匹配', rt_info
    else:
        infos('[WARING] 未找到匹配内容')
        return
    return rt_list_tuple


def _join_audio_address(tel_json_url):
    if tel_json_url:
        soup_msg = soup.request_headers(tel_json_url, headers=hd)
        # '"src":"http://audio.xmcdn.com/group28/M09/7C/CC/wKgJXFpU-VOhig-JAH5SJ9GCHxg708.m4a"'
        p_msg = re.findall(r'"src":"([^"]+)"', soup_msg)
        # print req.text
        if p_msg:
            return p_msg[0]


def _parse_track_id(r_url):
    track_id = re.search('.+/([^/]+)', r_url)
    if track_id:
        return track_id.group(1)
    errors('audio ID解析失败 URL>{}'.format(track_id))


def _join_audio_id(track_id):
    # 拼接音频访问明细主页，将ID带入请求路径
    if track_id:
        audio_url = 'http://www.ximalaya.com/revision/play/tracks?trackIds={track_id}'
        return audio_url.format(track_id=track_id)


def _get_audio_name(audio_url):
    audio_name = re.search('.+/([^/]+)', audio_url)
    if audio_name:
        return audio_name.group(1)
    else:
        return str(time.strftime("%Y%m%d%H%M", time.localtime())) + '.m4a'


def _clean_file_name(file_name):
    return re.sub('[/:*?"<>| ]', '-', file_name)


def download_audio_urls(list_audio, audio_name):
    if list_audio:
        infos('开始下载... TOTAL {}'.format(len(list_audio)))
        counter = 0
        global glb_path_save_urls
        init_path()

        if audio_name:
            clean_name = _clean_file_name(audio_name.decode('utf-8'))
            file_name = u'urls_audio_{}.txt'.format(clean_name)
        else:
            file_name = u'urls_audio_{}.txt'.format(curr_data_ymdhm())

        file_path = u'{source}/{name}'.format(source=glb_path_save_urls, name=file_name)
        print "path >>>  ", file_path
        with open(file_path, 'a') as files:
            for audio in list_audio:
                try:
                    audio_title, audio_url, audio_id = audio[0], audio[1], audio[2]
                    # audio_name = _get_audio_name(audio_url)
                    target_msg = '{url}@{title}@{id}@{name}'.format(url=audio_url, title=audio_title, id=audio_id,
                                                                    name=audio_name)
                    files.write(target_msg + '\n')
                    counter += 1
                except Exception, e:
                    errors('下载失败 URL > {}'.format(audio_url))
                    errors(e)
                    continue
        infos('下载完成！共计下载资源 {}个'.format(str(counter)))


def _find_audio_msg(tel_url):
    try:
        if tel_url:
            tel_url = tel_url.strip()
            soup_msg = soup.request(tel_url, headers=hd)
            # print req.text
            beaut_soup = BeautifulSoup(soup_msg, 'lxml')

            # type 1
            # tag_ele = soup.select('.e-997676211.lyric.hidden')
            # if tag_ele:
            #     return tag_ele[0].text
            # type 2
            tag_ele = beaut_soup.find_all("span", attrs={"style":
                                                             "font-size:16px;color:#333333;line-height:30px;word-break:break-all;font-family:Helvetica,Arial,sans-serif;font-weight:normal"})
            rt_msg = []
            for aa in tag_ele:
                rt_msg.append(aa.text + '\n')
            return ''.join(rt_msg)

    except:
        errors('未找到相关内容! URL>{}'.format(tel_url))


def get_page_num(page_total):
    page_size = 30

    if page_total and page_total > 0:
        page_counter = 0 if page_total % page_size == 0 else 1

        return page_total / page_size + page_counter
    else:
        return 1


def _save_and_load(audio_info):
    try:
        # step1 parse
        audio_arr = audio_info.split('@')
        audio_url, audio_name, track_url, file_name = \
            audio_arr[0].strip(), audio_arr[1].decode('utf8').strip(), audio_arr[2], audio_arr[3].strip()
        # audio_name = _get_audio_name(audio_url)
        global glb_path_save_audio
        time_start = curr_date_format()

        # step2 find audio
        file_second_path = os.path.join(glb_path_save_audio, file_name)
        if not os.path.exists(file_second_path):
            os.mkdir(file_second_path)

        audio_name = _clean_file_name(audio_name)

        file_target_path = os.path.join(file_second_path, audio_name)

        # clean_path = _clean_file_name(file_target_path)
        if not os.path.exists(file_target_path):
            os.mkdir(file_target_path)

        audio_title = audio_name + '.m4a'
        rt = soup.request(audio_url)
        infos('音频保存中 > {}'.format(audio_title))
        audio_save_name = os.path.join(file_target_path, audio_title)
        with open(audio_save_name, 'wb') as file_audio:
            file_audio.write(rt.content)

        # step3 save msg if exist
        # track_msg = _find_audio_msg(track_url)
        # if track_msg:
        #     audio_msg_title = audio_name + '.txt'
        #     audio_msg_path = os.path.join(file_target_path, audio_msg_title)
        #     infos('音频文本保存中 > {}'.format(audio_msg_path))
        #     with open(audio_msg_path, 'a') as file_audio_msg:
        #         file_audio_msg.write(track_msg)

        time_end = curr_date_format()
        infos("            >costing {}".format((time_end - time_start)))
    except Exception, e:
        errors('保存文件失败 file>{0},errMsg>{1}'.format(audio_info, e))


def download_audio():
    global glb_path_save_parse
    file_list = get_all_files_path_name(glb_path_save_parse)
    for file_msg in file_list:
        file_name, file_path = file_msg[0], file_msg[1]
        with open(file_path, 'r') as file_urls:
            infos('开始读取文件 > {}'.format(file_name))
            list_urls = file_urls.readlines()
            for audio_info in list_urls:
                _save_and_load(audio_info)

            infos('读取文件结束 >')


def start_find_cate_ids():
    # 通过首页 首页>有声书>文学  赛选内容，获取 ID 和 NAME
    tel_url = []
    base_url = '{tel_url}/p{page}'

    # wenxue_dangdai = 'https://www.ximalaya.com/youshengshu/wenxue/mr132t2722r227t3486/'
    # tel_url.append(wenxue_dangdai)
    # for index in range(2, 35):
    #     tel_url.append(base_url.format(tel_url=wenxue_dangdai, page=index))

    tel_url.append('https://www.ximalaya.com/diantai/xinwentai/')
    tel_url.append('https://www.ximalaya.com/diantai/xinwentai/p2')

    pattern = '"albumId":([^,]+),\s*"title":"([^"]+)"'

    re_msg = []
    for url in tel_url:
        soup_msg = soup.request_headers(url, headers=hd)
        beaut_soup = BeautifulSoup(soup_msg, 'lxml')
        msg_list = re.findall(pattern, beaut_soup.text)
        infos(msg_list)
        for msg in msg_list:
            msg = "{albumId}@{title}".format(albumId=msg[0], title=msg[1])
            re_msg.append(msg)

    infos('BEFORE > len[{}]'.format(len(re_msg)))
    sort_list = list(set(re_msg))
    infos('AFTER > len[{}]'.format(len(sort_list)))
    for msg in sort_list:
        arr = msg.split('@')
        print "{albumId}@{title}".format(albumId=arr[0], title=arr[1])


def start_parse_url_by_ids():
    global glb_path_save_config

    rt_msg = []
    files = get_all_files(glb_path_save_config)
    for file_name in files:
        file_path = os.path.join(glb_path_save_config, file_name)
        with open(file_path, 'r') as category:
            url_list = category.readlines()
            for url_msg in url_list:
                url_arr = url_msg.split('@')
                print url_arr[0], '@', url_arr[1]
                rt_msg.append((url_arr[0], url_arr[1]))
    return rt_msg


def start_find_all_category():
    url_list = start_parse_url_by_ids()
    if not url_list:
        errors('未找到解析文件，category！')
        return
    url = 'http://www.ximalaya.com/youshengshu/{track_id}'

    # 遍历所有路径开始下载URL任务
    for url_msg in url_list:

        # step1 获取audio总条数
        track_id, track_name = url_msg[0].strip(), url_msg[1].strip()
        tel_url = url.format(track_id=track_id)

        # req = requests.get(tel_url, headers=hd)
        soup_msg = soup.request_headers(tel_url, headers=hd)

        regex1 = u'专辑里的声音\(<!-- -->([0-9]+)<!-- -->\)'

        org = re.findall(regex1, soup_msg)
        if org:
            print '{}@{}@{}'.format(track_id, track_name, int(org[0]))
            # 调用保存方法
            # _save_and_load_batch(tel_url, track_name, int(org[0]))
        else:
            print '{}@{}  PAGE 查询失败'.format(track_id, track_name)
            continue

        # step2 计算分页总数 生成包括分页的所有访问路径
        page_num = get_page_num(int(org[0]))
        telurl_list = []
        telurl_list.append(tel_url)
        base_url = '{tel_url}/p{page}'
        if page_num > 1:
            for page in range(2, page_num + 1):
                telurl_list.append(base_url.format(tel_url=tel_url, page=page))

        # step3 保存每个分页的音频详情
        start_find_category(telurl_list, track_name)

        # if True:
        #     return


def get_tel_urls():
    tel_url = []
    base_url = '{tel_url}/p{page}'

    # tel_url = 'http://www.ximalaya.com/jiaoyu/353405/p2' # 朗读60篇
    # tel_url = ['http://www.ximalaya.com/jiaoyu/2808888/', 'http://www.ximalaya.com/jiaoyu/2808888/p2']
    # tel_url = ['http://www.ximalaya.com/youshengshu/7939039']
    #
    # base_url = 'http://www.ximalaya.com/youshengshu/7939039/p{page}'
    # for index in range(2, 12):
    #     tel_url.append(base_url.format(page=index))
    #     return tel_url

    # 《血玲珑》毕淑敏小说
    # tel_url = ['https://www.ximalaya.com/youshengshu/12373151/', 'https://www.ximalaya.com/youshengshu/12373151/p2/']

    # 黄金时代-王小波
    # tel_url = ['https://www.ximalaya.com/youshengshu/6905205/', 'https://www.ximalaya.com/youshengshu/6905205/p2/',
    #            'https://www.ximalaya.com/youshengshu/6905205/p3/']
    # 大宅门
    #
    # tel_url = ['https://www.ximalaya.com/youshengshu/14495260/', ]
    # for index in range(2, 6):
    #     tel_url.append(base_url.format(tel_url=tel_url[0], page=index))
    # return tel_url

    # 平凡的世界
    # url_ping_fan_shi_jie = 'https://www.ximalaya.com/youshengshu/2698626/'
    # tel_url.append(url_ping_fan_shi_jie)
    # for index in range(2, 5):
    #     tel_url.append(base_url.format(tel_url=url_ping_fan_shi_jie, page=index))
    # # # # 一地鸡毛
    # tel_url.append('https://www.ximalaya.com/youshengshu/2986949/')
    # #
    # # # # 韩寒-我所理解的生活
    # tel_url.append('https://www.ximalaya.com/youshengshu/335427/')
    # tel_url.append('https://www.ximalaya.com/youshengshu/335427/p2/')
    return tel_url


def start_find_category(tel_url=None, track_name=None):
    if not tel_url:
        tel_url = get_tel_urls()
    url_head = 'http://www.ximalaya.com'

    # step1
    list_tuple = []
    for each_url in tel_url:
        talking_list = get_talking_list(each_url)
        if talking_list:
            list_tuple.extend(talking_list)

    list_audio = []

    # step2
    if list_tuple:
        infos('成功获取地址条数： {}'.format(len(list_tuple)))
        for r_tup in list_tuple:
            r_name, r_url = r_tup[0], r_tup[1]
            track_id = _parse_track_id(r_url)
            tel_json_url = _join_audio_id(track_id)
            audio_url = _join_audio_address(tel_json_url)
            track_url = '{head}/{track}'.format(head=url_head, track=r_url)
            if audio_url:
                list_audio.append((r_name, audio_url, track_url))
            else:
                errors('处理异常：url>{r_tup},track_id>{track_id}'.format(r_tup=r_tup, track_id=track_id))
    # step3
    download_audio_urls(list_audio, track_name)
