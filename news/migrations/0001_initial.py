# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='publication date')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(help_text='Obsah bude prehnaný <a href="http://en.wikipedia.org/wiki/Markdown">Markdownom</a>.')),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='news_entries')),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
            options={
                'ordering': ('-pub_date',),
                'verbose_name_plural': 'novinky',
                'get_latest_by': 'pub_date',
                'verbose_name': 'novinka',
            },
            bases=(models.Model,),
        ),
    ]
