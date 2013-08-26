#coding=utf-8

import smtplib
import email
import mimetypes
import os.path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.header import Header
from config import *

def send_message(msg):
	smtp = smtplib.SMTP()
	print "start connecting"
	smtp.connect(MAIL_SERVER, MAIL_PORT)
	print "start login"
	smtp.login(USER_NAME, USER_PWD)
	try:
		smtp.sendmail(msg['From'], msg['To'], msg.as_string())
	except Exception, ex:
		print Exception, ex
		print "Error - send failed"
	else:
		print "send success!"
	smtp.quit()

"""
MIME添加附件
1.判断附件的类型guess_type返回类型和编码
2.如果是文本创建MIMEText，否则创建MIMEBase
3.创建MIMEMultipart
4.使用attach向MIMEMultipart中追加对象
"""

def build_attachment(filename):
	if len(filename) == 0:
		return None

	# print (filename)
	showname = os.path.basename(filename)
	fd = file(filename, "rb")
	mimetype, mimeencoding = mimetypes.guess_type(filename)
	if mimeencoding or (mimetype is None):
		mimetype = "application/octet-stream"
	maintype, subtype = mimetype.split("/")

	if maintype == "text":
		retval = MIMEText(fd.read(), _subtype = subtype, _charset = "utf-8")
	else:
		retval = MIMEBase(maintype, subtype)
		retval.set_payload(fd.read())
		email.encoders.encode_base64(retval)
	# fix:when the attachment name is Chinese
	showname = unicode(showname,"utf-8").encode("gb2312")
	retval.add_header("Content-Disposition","attachment",filename = showname)
	fd.close()
	return retval

def build_message(mailfrom, mailto, subject, content, attachment):
	msg = MIMEMultipart()
	msg['Mime-Version'] = '1.0'
	msg['From']    = "%s<%s>" % (Header("zhang三疯", "utf-8"), mailfrom)
	msg['To']      = "%s<%s>" % (Header("xiao龙女", "utf-8"), mailto)
	msg['Subject'] = Header(subject, "utf-8")
	msg['Date']    = email.Utils.formatdate()
	msg.attach(MIMEText(content, _subtype = "plain", _charset = "utf-8"))

	for x in xrange(0,len(attachment)):
		att = build_attachment(attachment[x])
		if att is not None:
			msg.attach(att)
	
	return msg

if __name__=="__main__":
	msg = build_message(MAIL_FROM, MAIL_TO, MAIL_SUBJECT, MAIL_CONTENT, MAIL_ATTACHMENT)
	print "build_message done!"
	print "start sending"
	send_message(msg)
