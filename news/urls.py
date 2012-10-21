from django.conf.urls import patterns, include, url
from django.contrib import admin

from news.views import EntryListView


urlpatterns = patterns('',
    url(r'^page/(?P<page>[0-9]+)/$', EntryListView.as_view(),
        name='news_list'),
)
