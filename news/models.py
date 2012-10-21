# coding: utf-8
from __future__ import unicode_literals
from django.db import models


class Entry(models.Model):
    author = models.ForeignKey('auth.User', related_name='news_entries')
    pub_date = models.DateTimeField(verbose_name='publication date', auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField(help_text='Obsah bude prehnaný <a '
                            'href="http://en.wikipedia.org/wiki/Markdown">'
                            'Markdownom</a>.')
    slug = models.SlugField()

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ('-pub_date',)
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return self.title
