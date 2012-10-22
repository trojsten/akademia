# coding: utf-8
from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator

from news.models import Entry


class NewsFeed(Feed):
    feed_type = feedgenerator.Atom1Feed
    title = "Novinky Akadémie Trojstenu"
    link = "/"
    subtitle = "Čo je nové ohľadom Akadémie a&nbsp;Klubu Trojstenu"

    def items(self):
        return Entry.objects.all()[:10]

    def item_link(self):
        return "/"

    def item_author_name(self, item):
        return item.author.username

    def item_pubdate(self, item):
        return item.pub_date

    def item_description(self, item):
        return item.rendered_text()
