# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
import  views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ishe.views.home', name='home'),
    url(r'^blog/', include('blog.urls')),
    url(r'^login/$',views.mylogin),
    url(r'^logout/$',views.mylogout),
    url(r'^register/$',views.register,name='register'),
    url(r'^chpwd/$',views.chpwd,name='chengpassword'),
    url(r'^admin/', include(admin.site.urls)),
)
