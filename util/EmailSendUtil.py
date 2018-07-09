# -*- coding: utf-8 -*-
# @Time    : 2018/1/31
# @Author  : LIYUAN134
# @File    : EmailSendUtil.py
# @Commment:
#
import smtplib
from poemUtil import random_poem
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_emails(content):
    try:
        from_addr = '18751845189@163.com'  # 发件人 地址及密码
        from_password = '@MICzdl37wznb123'

        # to_addr = 'newbaiha@163.com'  # 收件人地址
        to_addr = 'newbaiha@163.com'  # 收件人地址
        # to_addr = '4598369@qq.com'
        smtp_server = 'smtp.163.com'  # 邮件服务器，在对应邮箱的设置找下

        # send_msg = '近期工作内容<%s>' % str(content)
        # soups = '生死聚散，我曾经对你说过。拉着你的手，和你一起老去。唉，太久。让我无法（与你）相会。唉，太遥远，让我的誓言不能履行。'
        # soups += '瑟本怎么活有五十个弦，但即使这样它的每一弦、每一音节，足以表达对那美好年华的思念。庄周其实知道自己只是向往那自由自在的蝴蝶。望帝那美好的心灵和作为可以感动杜鹃。大海里明月的影子像是眼泪化成的珍珠。只有在彼时彼地的蓝田才能生成犹如生烟似的良玉。那些美好的事和年代，只能留在回忆之中了。而在当时那些人看来那些事都只是平常罢了，却并不知珍惜。'
        # send_msg = '近期工作内容' + soups
        # print send_msg
        send_msg = '近期工作内容'+''.join(random_poem())
        print send_msg
        msg = MIMEText(send_msg, 'plain', 'utf-8')
        msg['From'] = _format_addr('胜多负少的<%s>' % from_addr)  # 发件人命名
        msg['To'] = _format_addr('刘水电费<%s>' % to_addr)  # 收件人命名
        msg['Subject'] = Header(content, 'utf-8')  # Header(message)'工作进度汇报'
        server = smtplib.SMTP(smtp_server, 25)
        server.login(from_addr, from_password)
        server.sendmail(from_addr, to_addr, msg.as_string())

        server.quit()
    except Exception, e:
        print '邮件发送失败！', e
        return
    print '邮件发送成功！'


def qingxi():
    import re
    pattern = u'[<>《》！*(^)$%~!@#$…&%￥—+=、。，,；‘’“”：·`]'

    msg = u'你好,你,，。,!<>《》！*(^)$%~!@#$…&%￥—+=、。，,；‘’“”：·`'

    print re.sub(pattern, '', msg)


if __name__ == '__main__':
    send_emails('天眼任务搞定了!')
