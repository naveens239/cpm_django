from django.conf.urls import patterns, url
import api.views

urlpatterns = patterns(
	'api.views',
	url(r'^projects/$', 'project_list', name='project_list'),
	url(r'^schedules/$', 'schedule_list', name='schedule_list'),
	url(r'^schedules/(?P<pk>[0-9]+)/$', 'schedule_details', name='schedule_details'),
	url(r'^materials/$', 'material_list', name='material_list'),
	url(r'^materials/(?P<pk>[0-9]+)/$', 'material_details', name='material_details'),
	url(r'^status/$', 'status_list', name='status_list'),
	url(r'^prototypes/$', 'prototype_list', name='prototype_list'),
	url(r'^prototypes/(?P<pk>[0-9]+)/$', 'prototype_details', name='prototype_details'),
    url(r'^schedulecomments/$', 'schedule_comment_list', name='schedule_comment_list'),
    url(r'^ordercomments/$', 'order_comment_list', name='order_comment_list'),
	# url(r'^schedulecomments/(?P<pk>[0-9]+)/$', 'schedule_comment_details', name='schedule_comment_details'),

)