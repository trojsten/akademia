from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/news/page/1/')),
    url(r'^news/', include('news.urls')),
    url(r'^account/', include('ksp_login.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
