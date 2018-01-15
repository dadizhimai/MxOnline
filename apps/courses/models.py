# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


# Create your models here.
class Course(models.Model):
	name = models.CharField(max_length=50, verbose_name=u"课程名称")
	desc = models.CharField(max_length=300, verbose_name=u"课程描述")
	detail = models.TextField(verbose_name=u"课程详情")
	degree = models.CharField(max_length=10, choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), verbose_name=u"课程级别")
	learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟）")
	students = models.IntegerField(default=0, verbose_name=u"学习人数")
	fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
	image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"课程展示封面")
	click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
	add_time = models.DateField(default=datetime.now, verbose_name=u"课程创建时间")

	class Meta:
		verbose_name = "课程基本信息"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name


class Lesson(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程")
	name = models.CharField(max_length=100, verbose_name=u"章节名")
	add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = "章节基本信息"
		verbose_name_plural = verbose_name

	def __unicode__(self):
		return self.name


class Video(models.Model):
	lesson = models.ForeignKey(Lesson, verbose_name=u"章节名")
	name = models.CharField(max_length=100, verbose_name=u"视频名")
	add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = "视频基本信息"
		verbose_name_plural = verbose_name


class CourseResource(models.Model):
	course = models.ForeignKey(Course, verbose_name=u"课程")
	name = models.CharField(max_length=100, verbose_name=u"名称")
	download = models.FileField(max_length=100, upload_to="course/resource/%Y/%m", verbose_name=u"资源下载")
	add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

	class Meta:
		verbose_name = "资源基本信息"
		verbose_name_plural = verbose_name
