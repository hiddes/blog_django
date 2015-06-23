# coding=utf-8
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^edit/$',views.edit_blog,name='edit_blog'),
    url(r'^addtag/$',views.add_tag,name='add_tag'),
    url(r'^messbox/$',views.messbox,name='add_tag'),
    url(r'^showbox/$',views.showbox,name='showbox'),
    # url(r'^addcls/$',views.add_cls,name='add_cls'),
    url(r'^editinfo/$',views.edit_info,name='edit_info'),
    url(r'^(?P<id>[0-9]+)/$',views.view_blog,name='view_blog'),

)