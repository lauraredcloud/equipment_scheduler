from django.conf.urls import patterns, url

from scheduler import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<item_id>\d+)/$', views.detail, name='detail')
)