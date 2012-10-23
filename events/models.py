# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.sites.models import Site


class School(models.Model):
    abbreviation = models.CharField(max_length=23,
                                    blank=True,
                                    verbose_name="skratka",
                                    help_text="Sktatka názvu školy.")
    verbose_name = models.CharField(max_length=47,
                                    verbose_name="celý názov")
    addr_name = models.CharField(max_length=47, blank=True)
    street = models.CharField(max_length=47, blank=True)
    city = models.CharField(max_length=47, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "škola"
        verbose_name_plural = "školy"
        ordering = ("verbose_name",)

    def __unicode__(self):
        return self.verbose_name


class AdditionalUserDetails(models.Model):
    user = models.OneToOneField('auth.User')
    school = models.ForeignKey(School, default=1,
                               help_text='Pokiaľ vaša škola nie je '
                               'v&nbsp;zozname, vyberte "Gymnázium iné" '
                               'a&nbsp;pošlite nám e-mail.')
    is_teacher = models.BooleanField(verbose_name="som učiteľ")

    class Meta:
        verbose_name = "dodatočné údaje o užívateľoch"
        verbose_name_plural = "dodatočné údaje o užívateľoch"

    def __unicode__(self):
        return "%s" % (self.user,)


class Event(models.Model):
    name = models.CharField(max_length="47",
                            help_text="Názov akcie, napr. Klub Trojstenu "
                            "po Náboji FKS")
    date = models.DateField()
    deadline = models.DateTimeField()
    sites = models.ManyToManyField(Site)

    class Meta:
        verbose_name = "akcia"
        verbose_name_plural = "akcie"
        ordering = ("-date",)

    def __unicode__(self):
        return "%s %s" % (self.name, self.date.year)


class Lecture(models.Model):
    event = models.ForeignKey(Event, verbose_name="akcia",
                              related_name="lectures")
    lecturer = models.CharField(max_length=47, verbose_name="prednášajúci")
    title = models.CharField(max_length=147, verbose_name="názov prednášky")
    abstract = models.TextField(verbose_name="abstrakt")
    room = models.CharField(max_length=20, verbose_name="miestnosť")
    time = models.TimeField(verbose_name="čas")
    video_url = models.URLField(verbose_name="URL videa")

    class Meta:
        verbose_name = "prednáška"
        verbose_name_plural = "prednášky"
        ordering = ("event", "time")
