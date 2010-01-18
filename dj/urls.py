from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from main.models import *

databrowse.site.register(Client)
databrowse.site.register(Show)
databrowse.site.register(Location)
databrowse.site.register(Episode)
databrowse.site.register(Raw_File)
databrowse.site.register(Cut_List)


urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    ('^$', redirect_to, {'url': '/main/'}),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/(.*)', include(admin.site.urls) ),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^main/', include('main.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
)

urlpatterns += patterns('',
(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static/','show_indexes': True}))

urlpatterns += patterns('',
(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/juser/Videos/veyepar/','show_indexes': True}))

