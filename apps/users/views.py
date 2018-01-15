# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm

# Create your views here.


class CustomBackends(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 使用get只能返回一个，相当于一个验证
			if user.check_password(password):
				return user
		except Exception as e:
			return None


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
				return render(request, 'login.html', {'message': '用户名或密码错误2'})
		else:
			return render(request, 'login.html', {'login_form': login_form})







