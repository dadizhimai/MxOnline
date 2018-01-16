# -*- coding:utf-8 -*-
__author__ = '@Able.Tiger'
__date__ = '2018/1/15 11:06'

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=6)
	captcha = CaptchaField()
