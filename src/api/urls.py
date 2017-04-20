from django.conf.urls import url, include
from django.contrib import admin
from . import views
urlpatterns = [
	#'api.views',
	#url(r'^projects/$', 'project_list', name='project_list'),
	#url(r'^schedules/$', 'schedule_list', name='schedule_list'),
	#url(r'^schedules/(?P<pk>[0-9]+)/$', 'schedule_details', name='schedule_details'),
	#url(r'^materials/$', 'material_list', name='material_list'),
	#url(r'^materials/(?P<pk>[0-9]+)/$', 'material_details', name='material_details'),
	#url(r'^status/$', 'status_list', name='status_list'),
	#url(r'^prototypes/$', 'prototype_list', name='prototype_list'),
	#url(r'^prototypes/(?P<pk>[0-9]+)/$', 'prototype_details', name='prototype_details'),
    #url(r'^schedulecomments/$', 'schedule_comment_list', name='schedule_comment_list'),
    #url(r'^ordercomments/$', 'order_comment_list', name='order_comment_list'),
	## url(r'^schedulecomments/(?P<pk>[0-9]+)/$', 'schedule_comment_details', name='schedule_comment_details'),
    url(r'^projects/$', views.project_list),
	url(r'^schedules/$', views.schedule_list),
	url(r'^schedules/(?P<pk>[0-9]+)/$', views.schedule_details),
	url(r'^materials/$', views.material_list),
	url(r'^materials/(?P<pk>[0-9]+)/$', views.material_details),
	url(r'^status/$', views.status_list),
	url(r'^prototypes/$', views.prototype_list),
	url(r'^prototypes/(?P<pk>[0-9]+)/$', views.prototype_details),
    url(r'^schedulecomments/$', views.schedule_comment_list),
    url(r'^ordercomments/$', views.order_comment_list),
	
]