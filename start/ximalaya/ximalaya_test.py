# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 
# @Author  : ErichLee ErichLee@qq.com
# @File    : ximalaya_test.py
# @Comment : 
#            

import sys
import requests
import os
from util.loggerUtil import *

reload(sys)
sys.setdefaultencoding('utf-8')


def download():
    url = 'http://audio.xmcdn.com/group28/M09/7C/CC/wKgJXFpU-VOhig-JAH5SJ9GCHxg708.m4a'
    rt = requests.get(url)

    with open('aa.m4a', 'ab') as ss:
        ss.write(rt.content)


def _save_and_load_batch(audio_url, audio_name):
    print audio_url, audio_name

    if True:
        return

    global glb_path_save_audio
    file_second_path = os.path.join(glb_path_save_audio, audio_name)
    if not os.path.exists(file_second_path):
        os.mkdir(file_second_path)

    audio_title = audio_name + '.m4a'

    rt = requests.get(audio_url)
    infos('音频保存中 > {}'.format(audio_title))
    audio_save_name = os.path.join(file_second_path, audio_title)
    with open(audio_save_name, 'wb') as file_audio:
        file_audio.write(rt.content)
