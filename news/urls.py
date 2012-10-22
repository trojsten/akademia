from django.conf.urls import patterns, include, url
from django.contrib import admin

from news.views import EntryListView
from news.feeds import NewsFeed


urlpatterns = patterns('',
    url(r'^page/(?P<page>[0-9]+)/$', EntryListView.as_view(),
        name='news_list'),
    url(r'^feed/$', NewsFeed(), name='news_feed'),
)
