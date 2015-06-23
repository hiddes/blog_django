# coding:utf-8
#中文注释
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#博客标签
class Tag(models.Model):
    name = models.CharField(max_length=30,verbose_name='标签')
    class Meta:
        verbose_name = '标签'
        ordering =['id']
    def __unicode__(self):
        return self.name

#博客分类
class Cls(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        verbose_name = '类别'
        ordering = ['id']
    def __unicode__(self):
        return self.name

#定义博客数据块
class blog(models.Model):
    title = models.CharField(max_length=50,verbose_name='标题')
    desc = models.TextField(verbose_name='描述')
    clss = models.ManyToManyField(Cls,verbose_name='分类')
    timestamp =models.DateField(auto_now_add=True,verbose_name='发布时间')
    autor = models.ForeignKey(User,verbose_name='作者')
    tag = models.ForeignKey(Tag,verbose_name='标签')
    text = models.TextField(verbose_name='内容')
    class Meta:
        verbose_name = '博客'
        ordering = ['-timestamp']
    def __unicode__(self):
        return self.title

#定义用户信息(扩展)
class userinfo(models.Model):
    user = models.ForeignKey(User,verbose_name='用户名')
    sign = models.CharField(max_length=100,verbose_name='签名')
    pothon = models.CharField(max_length=20,verbose_name='电话')
    qq  = models.CharField(max_length=20,verbose_name='QQ')

    class Meta:
        verbose_name = '用户信息'
    def __unicode__(self):
        return self.sign

#留言板
class MBox(models.Model):
    fromuser = models.CharField(max_length=20,verbose_name='留言者')
    touser = models.CharField(max_length=20,verbose_name='留给谁？')
    text = models.TextField(verbose_name='内容')
    timestamp = models.DateField(auto_now_add=True,verbose_name='时间')

    class Meta:
        verbose_name = '留言板'
        ordering = ['-timestamp']
    def __unicode__(self):
        return self.text