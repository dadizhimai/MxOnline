# -*- coding:utf-8 -*-

__author__ = '@Able.Tiger'
__date__ = '2018/1/16 10:36'
from random import Random
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
	str = ''
	chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
	length = len(chars)-1
	random = Random()
	for i in range(randomlength):
		str += chars[random.randint(0, length)]
	return str


def send_register_email(email, send_type='register'):
	email_record = EmailVerifyRecord()  # 实例邮箱验证类
	code = random_str(16)
	email_record.email = email
	email_record.code = code
	email_record.send_type = send_type
	email_record.save()

	email_title = ""
	email_body= ''

	if send_type == 'register':
		email_title = '暮雪在线网注册激活链接'
		email_body = '请点击下面的链接激活激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)

		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass
	elif send_type == 'forget':
		email_title = '暮雪在线网重置密码链接'
		email_body = '请点击下面的链接重置密码：http://127.0.0.1:8000/pwd_reset/{0}'.format(code)

		send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
		if send_status:
			pass