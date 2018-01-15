# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm

# Create your views here.


class CustomBackends(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 使用get只能返回一个，相当于一个验证
			if user.check_password(password):
				return user
		except Exception as e:
			return None


# 注册
class RegisterView(View):
	def get(self, request):
		return render(request, 'register.html')

	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			email = request.POST.get('email', '')
			password = request.POST.get('password', '')
			captcha_1 = request.POST.get('captcha_1', '')
			# 保存用户数据表
			user = UserProfile()
			user.email = email
			user.password = password
			user.save()
			# 保存验证码表
			emailVerifyRecord = EmailVerifyRecord()
			emailVerifyRecord.code = captcha_1
			emailVerifyRecord.email = email
			emailVerifyRecord.save()
			return render(request, 'index.html', locals())

			pass
		else:
			return render(request, 'register.html', {'register_form': register_form})


# 登录
class LoginView(View):

	def get(self, request):
		return render(request, 'login.html', locals())

	def post(self, request):
		login_form = LoginForm(request.POST)
		if login_form.is_valid():   # 验证form
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user = authenticate(username=username, password=password)  # 验证登录名和密码
			if user is not None:
				login(request, user)
				user_detail = UserProfile.objects.get(Q(username=username) | Q(email=username))
				return render(request, 'index.html', locals())
			else:
				return render(request, 'login.html', {'message': '用户名或密码错误！'})
		else:
			return render(request, 'login.html', {'login_form': login_form})







