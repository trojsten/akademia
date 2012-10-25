from django.conf.urls import patterns, include, url
from django.contrib import admin

from akademia.views import IndexView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^news/', include('news.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^account/', include('ksp_login.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^', include('django.contrib.flatpages.urls')),
)
