# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='poll',
            field=models.ForeignKey(related_name='lectures', null=True, help_text='Anketa', to='polls.Poll', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='individualsignup',
            name='event',
            field=models.ForeignKey(related_name='individual_signups', to='events.Event', verbose_name='akcia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='individualsignup',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='poll',
            field=models.ForeignKey(related_name='events', null=True, help_text='Anketa', to='polls.Poll', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='additionaluserdetails',
            name='school',
            field=models.ForeignKey(default=1, help_text='Do políčka napíšte skratku, časť názvu alebo adresy školy a následne vyberte správnu možnosť zo zoznamu. Pokiaľ vaša škola nie je v&nbsp;zozname, vyberte "Gymnázium iné" a&nbsp;pošlite nám e-mail.', to='events.School', verbose_name='škola'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='additionaluserdetails',
            name='user',
            field=models.OneToOneField(related_name='additional_events_details', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
