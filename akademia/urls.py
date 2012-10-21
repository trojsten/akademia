from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^account/', include('ksp_login.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
