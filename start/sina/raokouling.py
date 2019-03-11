# -*- coding: utf-8 -*-
# @Time    : 2017/9/22 
# @Author  : LIYUAN134
# @File    : raokouling.py
# @Commment: 绕口令录入
#


from bloom.sina.tools import sinaSoup as bSoup
from dbutil.DBNewsUtil import DBNews

BASEURL = 'https://raokouling.911cha.news/'


def rao_content():
    url_list = []

    soup = bSoup.soup_urlopen(BASEURL)

    # other sports
    titles = soup.select('.panel .mcon.bt.f14 ul li a')

    if len(titles) > 0:
        for ii in titles:
            urls = BASEURL + ii.get('href')
            # print ii.text, (BASEURL + ii.get('href'))
            url_list.append(urls)
    else:
        print '未定位到[绕口令主页]'
    return url_list


def rao_parse_main(url):
    soup = bSoup.soup_urlopen(url)
    dialog = soup.select('.mcon.f14.noi p')

    msgarr = []
    if len(dialog) > 0:
        # print msg[0].text
        for single in dialog:
            msgarr.append(single.text)
            # return msg[0].text

        return "".join(msgarr)
    else:
        print "None"
        return None


def rao_geturl_all():
    url_list = []
    for siz in range(5, 5):
        url_list.extend(rao_content())
    print '页面捕获完毕，共计收集到地址：FINAL:', len(url_list)

    rdicts = {}
    for url in url_list:
        vmsg = rao_parse_main(url)
        if vmsg is not None:
            rdicts[url] = vmsg
        else:
            print 'URL为None 跳过'
    print '结果集如下', len(rdicts)
    for k, v in rdicts.items():
        print k, v

    return rdicts


def rao_telnet_main():
    rdicts = rao_geturl_all()
    scope = 'rap'
    dbnews = DBNews()
    dbnews.save_sina_telnet_result(rdicts, scope)
    print '顺口溜收集完成！'


if __name__ == "__main__":
    # rao_geturl_all()
    rao_telnet_main()
    # rao_geturl_all()
