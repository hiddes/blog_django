# coding=utf-8
from django.shortcuts import render
from models import blog,Tag,Cls
from forms import userinfo,blogF,tagF,userinfoF,clsF,mbF,MBox
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
@login_required
def index(req):
    if req.user.is_authenticated():
        blog_list = blog.objects.all().filter(autor_id=req.user.id)
    return render(req,'index.html',{'blogs':blog_list,'name':req.user.username,'loged':1})
@login_required
def edit_blog(req):
    error = []
    form = blogF()
    if req.method =="POST":
        form = blogF(req.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            text = form.cleaned_data['text']
            tag = form.cleaned_data['tag']
            # clss = form.cleaned_data['clss']
            autor = req.user
            if not blog.objects.all().filter(title=title,text=text):
                blog.objects.create(title=title,desc=desc,autor=autor,tag=tag,text=text)
            return HttpResponseRedirect('/blog')
        else:
            error.append('提交的数据不合法')
    else:
        form = blogF()
    return render(req,'edit_blog.html',{'form':form,'error':error,'loged':1})
@login_required
def add_tag(req):
    mess = []
    form = tagF()
    form2 = clsF()
    if req.method=="POST":
        form = tagF(req.POST)
        form2 =clsF(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            if not Tag.objects.all().filter(name=name):
                Tag.objects.create(name=name)
                mess.append("添加标签成功")
        else:
            if form2.is_valid():
                name = form.cleaned_data['name']
                Cls.objects.create(name=name)
                mess.append("添加分类成功")
            else:
                mess.append('添加的数据不合法')
    return render(req,'add_tag.html',{'form':form,'form2':form2,'mess':mess,'loged':1})
@login_required
def add_cls(req):
    mess =[]
    form = clsF()
    if req.method=="POST":
        form = clsF(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Cls.objects.create(name=name)
            mess.append('添加分类成功')
        else:
            mess.append('添加的数据不合法')
    return render(req,'add_class.html',{'form':form,'mess':mess,'loged':1})

#指定id的博客
def view_blog(req,id):
    req.user.is_authenticated()
    num = int(id)
    body = blog.objects.all().filter(id=num)
    return render(req,'blog_view.html',{'body':body[0],'loged':req.user.is_authenticated()})

#获取添加过的标签
def gettag(req):
    li = []
    tag = Tag.objects.all()
    for item in tag:
        li.append(item.name)
    return li

#添加附加信息
@login_required
def edit_info(req):
    #信息
    info = []
    info.append(req.user.username)
    info.append(req.user.email)
    message = []
    form = userinfoF()
    #存在用户信息
    if userinfo.objects.all().filter(user=req.user):
            sinfo = userinfo.objects.get(user=req.user)
            info.append(sinfo.pothon)
            info.append(sinfo.qq)
            info.append((sinfo.sign))
            # form = userinfoF(qq=sinfo.qq,sign=sinfo.sign,pothon=sinfo.pothon)
            if req.method == "POST":
                form = userinfoF(req.POST)
                sinfo.qq = form.cleaned_data['qq']
                sinfo.sign = form.cleaned_data['sign']
                sinfo.pothon = form.cleaned_data['pothon']
                sinfo.save()
                message.append('信息修改成功')
            return render(req,'edit_info.html',{'form':form,'info':info,'message':message,'loged':1,'tag':gettag(req)})
    else:
        if req.method=='POST':
            form = userinfoF(req.POST)
            if form.is_valid():
                usinfo = userinfo()
                usinfo.qq = form.cleaned_data['qq']
                usinfo.sign = form.cleaned_data['sign']
                usinfo.pothon = form.cleaned_data['pothon']
                usinfo.user = req.user
                usinfo.save()
                message.append('信息添加成功！！！')
        else:
            form = userinfoF()
        return render(req,'edit_info.html',{'form':form,'message':message,'loged':1,'info':info,'tag':gettag(req)})

#检查重复提交的数据
def checkbox(req,form):
    #匿名用户重复提交，不得行
    if MBox.objects.filter(touser=form.cleaned_data['text']) and not req.user.is_authenticated():
        return False
    else:
        return True
#留言
def messbox(req):
    error = []
    loged = req.user.is_authenticated()
    form = mbF()
    if req.method=="POST":
        form = mbF(req.POST)
        if form.is_valid():
            touser = form.cleaned_data['touser']
            if loged:
                fromuser = req.user.username
            else:
                fromuser = '路人甲'
            text = form.cleaned_data['text']
            if checkbox(req,form):
                MBox.objects.create(touser=touser,fromuser=fromuser,text=text)
                return HttpResponseRedirect('/blog/showbox')
            else:
                error.append('您已经提交过数据了！')
        else:
            error.append('请提交完整的数据。。')
    else:
        form =mbF()
    return render(req,'box.html',{'form':form,'error':error,'loged':loged})

def showbox(req):
    loged = req.user.is_authenticated()
    li=[]
    bl =[]
    #传一个二维数组，方便
    boxs = MBox.objects.all()
    for box in boxs:
        # bl.append(box.fromuser)
        # bl.append(box.text)
        # bl.append(box.touser)
        li.append(box)
    return render(req,'showbox.html',{'li':li,'loged':loged})