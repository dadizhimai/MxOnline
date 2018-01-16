# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import  make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, PwdResetForm
from utils.email_send import send_register_email

# Create your views here.


class CustomBackends(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 使用get只能返回一个，相当于一个验证
			if user.check_password(password):
				return user
		except Exception as e:
			return None


# 激活验证
class ActiveUserView(View):
	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email  # 取出邮箱激活验证码一样的邮箱
				user = UserProfile.objects.get(email=email)
				user.is_active = True  # 修改激活字段为True
				user.save()
		else:
			return render(request, 'active_fail.html')
		return render(request, 'login.html')


# 注册
class RegisterView(View):

	def get(self, request):
		register_form = RegisterForm()
		return render(request, 'register.html', {'register_form': register_form})

	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			email = request.POST.get('email', '')
			if UserProfile.objects.filter(email=email):
				return render(request, 'register.html', {'register_form': register_form, 'message': u'用户已经存在'})
			password = request.POST.get('password', '')
			# 保存用户数据表
			user = UserProfile()
			user.email = email
			user.username = email
			user.password = make_password(password)
			user.is_active = False
			user.save()
			# 发送邮箱验证激活
			send_register_email(email, 'register')
			return render(request, 'index.html', locals())
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
				if user.is_active:  # 验证是否激活
					login(request, user)
					# user_detail = UserProfile.objects.get(Q(username=username) | Q(email=username))
					return render(request, 'index.html', locals())
				else:
					return render(request, 'login.html', {'message': '用户未激活！'})
			else:
				return render(request, 'login.html', {'message': '用户名或密码错误！'})
		else:
			return render(request, 'login.html', {'login_form': login_form})


# 找回秘密
class ForgetPasswordView(View):
	def get(self, request):
		forget_pwd_form = ForgetPasswordForm()
		return render(request, 'forgetpwd.html', locals())

	def post(self, request):
		forget_pwd_form = ForgetPasswordForm(request.POST)
		if forget_pwd_form.is_valid():
			email = request.POST.get('email', '')
			# 找回密码发送邮件认证
			send_register_email(email, 'forget')
			return render(request, 'send_success.html')
		else:
			{'message': u'用户名错误,请重新输入！'}
			return render(request, 'forgetpwd.html', locals())


# 重置密码
class PwdResetView(View):
	def get(self, request, active_code):
		all_records = EmailVerifyRecord.objects.filter(code=active_code)
		if all_records:
			for record in all_records:
				email = record.email  #
				return render(request, 'password_reset.html', locals())
		else:
			return render(request, 'active_fail.html')

	def post(self, request):
		reset_pwd_form = PwdResetForm(request.POST)
		if reset_pwd_form.is_valid():
			password = request.POST.get('password', '')
			password2 = request.POST.get('password2', '')
			email = request.POST.get('email', '')
			if password == password2:
				user = UserProfile.objects.filter(email=email)
				user.password = make_password(password)
				user.save()
				return render(request, 'login.html')
			else:
				return render(request, 'password_reset.html',{'meg': u'两次密码不一样'})


		else:
			return render(request, 'password_reset.html', locals())



