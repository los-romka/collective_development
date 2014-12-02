from django.conf.urls import patterns, include, url
from frontend.views import *
from settings import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'photoplus.views.home', name='home'),
    # Examples:
    url(r'^$',home),
    url(r'^page/$',home),
    url(r'^page/(?P<page>\d+)/$',home_page),
    
    # url(r'^preview/(?P<idP>\d+)/$', preview),
    url(r'^preview/(?P<photoId>\d+)/$', preview),
    url(r'^buy/(?P<idP>\w+)/(?P<resolution>\w+)/$', buy),
    
    url(r'^about/feedback/', contact),
    #url(r'^about/buy/', buy),

    url(r'^captcha/', include('captcha.urls')),
    
    url(r'^about/$', about),
    url(r'^order/(?P<idOrder>\d+)/$', order),
    
    url(r'^albums/(?P<idA>\d+)/$', album),
    url(r'^albums/(?P<idA>\d+)/(?P<page>\d+)/$', album),

    url(r'^admin/forced_refresh/(?P<mode>\d+)$',forced_refresh),
    url(r'^admin/frontend/forced_refresh/(?P<mode>\d+)$',forced_refresh),
    url(r'^admin/auth/forced_refresh/(?P<mode>\d+)$',forced_refresh),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    { 'document_root': STATIC_ROOT }),
)


