# coding=utf-8
#定义博客中要用到的表单
from django.forms import ModelForm,Form
from django import forms
from blog.models import blog,userinfo,Tag,Cls,MBox

#博客标签输入表单
class tagF(ModelForm):
    class Meta:
        model = Tag
#分类
class clsF(ModelForm):
    class Meta:
        model = Cls

#注册表
class regF(Form):
    username = forms.CharField(label='用户名')
    email = forms.EmailField(label='电子邮箱')
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput)
    #检测两次输入的密码是否相同
    def pwd_validate(self):
        return self.cleaned_data['password'] == self.cleaned_data['password2']

#用户登录表单
class loginF(Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
    #是否自动登录
    # auto = forms.RadioChoiceInput()

#用户扩展信息表单
class userinfoF(ModelForm):
    class Meta:
        model = userinfo
        fields = ('sign','pothon','qq')

#博客编辑表单
class blogF(ModelForm):
    class Meta:
        model=blog
        fields = ('title','desc','text','tag')

#密码修改表单
class chpwdF(Form):
    oldpasswd = forms.CharField(widget=forms.PasswordInput)
    newpasswd = forms.CharField(widget=forms.PasswordInput)

class mbF(ModelForm):
    class Meta:
        model=MBox
        fields = ('text','touser')