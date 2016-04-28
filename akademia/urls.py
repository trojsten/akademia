from django.conf.urls import include, url
from django.contrib import admin

from akademia.views import IndexView


admin.autodiscover()

urlpatterns = [
    url(r'^$', IndexView.as_view()),
    url(r'^news/', include('news.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^account/', include('ksp_login.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
