from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^scheduler/', include('scheduler.urls', namespace="scheduler")),
    url(r'^admin/', include(admin.site.urls)),
)

# Add this to get widgets.AdminDateWidget() working for non is_staff, is_superuser
# This must be placed before (r'^admin/(.*)', admin.site.root), as that gobals up everything
(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
