#-*- coding:utf-8 -*-
import requests
import json
import sys
import traceback
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.yeah.net"                  # SMTP服务器
mail_user = "workrobot@yeah.net"             # 用户名
mail_pass = "QUSONZJDVULUWADO"               # 授权密码，非登录密码

sender = 'workrobot@yeah.net'    # 发件人邮箱(最好写全, 不然会失败)
receivers = ['15979627228@139.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

def sendEmail(title, content):
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except Exception as e:
        # 这个是输出错误的具体原因，这步可以不用加str，输出
        print('str(e):\t\t', str(e))  # 输出 str(e):            integer division or modulo by zero
        print('repr(e):\t', repr(e))  # 输出 repr(e):   ZeroDivisionError('integer division or modulo by zero',)
        print('traceback.print_exc():')
        # 以下两步都是输出错误的具体位置的
        print(traceback.print_exc())
        print('traceback.format_exc():\n%s' % traceback.format_exc())

def wxgroup(msg, users="lisensen"):
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a47bc760-e0f7-44ad-9f61-cb91a25fc6de"
    headers = {'Content-Type': 'application/json'}
    text = dict({"content": msg, "mentioned_list": [users]})
    message = {"msgtype": "text", "text": text}
    response = requests.post(url, headers=headers, data=json.dumps(message))
    print(response.text)

def printMsg(msg):
    wxgroup(msg, "lisensen")
    print(msg)

if __name__ == "__main__":
    msg = sys.argv[1]
    wxgroup(msg,"lisensen")