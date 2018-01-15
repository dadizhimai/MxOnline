# -*- coding:utf-8 -*-
__author__ = '@Able.Tiger'
__date__ = '2018/1/15 11:06'

from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, min_length=5)




