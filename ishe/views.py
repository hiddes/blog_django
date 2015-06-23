# coding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate,login ,logout
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from blog.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#定义住页面
def home(req):
    loged = req.user.is_authenticated()
    li = blog.objects.all().order_by('-timestamp')
    return render(req,'home.html',{'blogs':li,'loged':loged})
#登录验证函数
def login_validate(req,username,passwd):
    #认证，加密算法是‘pbkdf2_sha256’    调用check_password对比
    user = authenticate(username=username,password=passwd)
    if user is not None:
        #django的login函数
        login(req,user)
        return True
    else:
        return False

#自定义登录
def mylogin(req):
    #定义一个变量，判断是否已经登录
    loged = req.user.is_authenticated()
    error = []
    form = None
    #检查是否已经登录
    if loged:
        return HttpResponseRedirect('/')
    else:
        if req.method == "POST":
            form = loginF(req.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                passwd = form.cleaned_data['password']
                if login_validate(req,username,passwd):
                    user = User.objects.get(username=username)
                    return render(req,'welcom.html',{'user':user})
                else:
                    error.append('请输入正确的密码！！！')
            else:
                error.append('请输入用户名和密码！！！')
        else:
            form = loginF()
    return render(req,'login.html',{'error':error,'form':form,'loged':loged})

#注册
def register(req):
    loged = req.user.is_authenticated()
    if loged:
        return HttpResponseRedirect('/')
    error  = []
    form = regF()
    if req.method=="POST":
        form = regF(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            passwd = form.cleaned_data['password']
            if not User.objects.all().filter(username=username):
                if form.pwd_validate():
                    #这里密码是明文的，加密方式是'pbkdf2_sha256'，加密存储（安全考虑）
                    passwds = make_password(passwd,hasher='pbkdf2_sha256')
                    User.objects.create(username = username,email=email,password=passwds)
                    if login_validate(req,username,passwd):
                        user = User.objects.get(username=username)
                        return render(req,'welcom.html',{'user':user})
                else:
                    error.append('Please input the same password  相同的密码')
            else:
                error.append('该用户已存在，请换个更好听的名字吧！')
        else:
            error.append('请检查您输入的数据是否完善！')
    else:
        form = regF()
    return render(req,'register.html',{'form':form,'error':error,'loged':loged})

#自定义登出
@login_required
def mylogout(req):
    logout(req)
    return HttpResponseRedirect('/login')

#更改密码
@login_required
def chpwd(req):
    error = []
    if req.method=='POST':
        form = chpwdF(req.POST)
        if form.is_valid():
            username = req.User.username
            oldpass = form.cleaned_data['oldpasswd']
            newpass = form.cleaned_data['newpasswd']
            user = authenticate(username=username,password=make_password(oldpass,'','pbkdf2_sha256'))
            if user is not None:
                if newpass==oldpass:
                    error.append('您的密码不能和原来的密码一样！！！')
                else:
                    user = User.objects.get(username=username)
                    user.password=newpass
                    user.save()
                    error.append('密码修改成功！！！')
            else:
                error.append('请输入正确的密码，谢谢！')
        else:
            error.append('请检查您的输入！！！')
    else:
        form = chpwdF()
    return render(req, 'chpwd.html',{'form':form})
