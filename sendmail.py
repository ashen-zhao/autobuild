#!/usr/bin/env python
#coding: utf-8

# sendEmail title content
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'xxxxx'
receiver = '122268149@qq.com'
smtpserver = 'smtp.exmail.qq.com'

username = sender
password = 'xxxxx'

def send_mail(title, content):

    try:
        msg = MIMEText(content,'plain','utf-8')
        if not isinstance(title,unicode):
            title = unicode(title, 'utf-8')
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = receiver
        msg["Accept-Language"]="zh-CN"
        msg["Accept-Charset"]="ISO-8859-1,utf-8"
        msg['CC'] = 'zhaoashen@gmail.com;zhaoas@uubee.com;apple_developer@uubee;'

        smtp = smtplib.SMTP_SSL(smtpserver,465)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print "邮件发送成功!"
        return True
    except Exception, e:
        print str(e)
        print "邮件发送失败!"
        return False
