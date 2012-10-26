# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.contrib.sites.models import Site
from django.utils.datastructures import SortedDict


class School(models.Model):
    abbreviation = models.CharField(max_length=100,
                                    blank=True,
                                    verbose_name="skratka",
                                    help_text="Sktatka názvu školy.")
    verbose_name = models.CharField(max_length=100,
                                    verbose_name="celý názov")
    addr_name = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "škola"
        verbose_name_plural = "školy"
        ordering = ("verbose_name",)

    def __unicode__(self):
        return self.verbose_name


class AdditionalUserDetails(models.Model):
    user = models.OneToOneField('auth.User')
    school = models.ForeignKey(School, default=1, verbose_name="škola",
                               help_text='Pokiaľ vaša škola nie je '
                               'v&nbsp;zozname, vyberte "Gymnázium iné" '
                               'a&nbsp;pošlite nám e-mail.')
    is_teacher = models.BooleanField(verbose_name="som učiteľ",
                                     help_text='Učitelia vedia hromadne '
                                     'prihlasovať školy na akcie.')
    graduation = models.IntegerField(blank=True, null=True,
                                     verbose_name="rok maturity")
    want_news = models.BooleanField(verbose_name="pozvánky e-mailom",
                                    help_text="Mám záujem dostávať "
                                    "e-mailom pozvánky na ďalšie akcie.")

    class Meta:
        verbose_name = "dodatočné údaje o užívateľoch"
        verbose_name_plural = "dodatočné údaje o užívateľoch"

    def __unicode__(self):
        return "%s" % (self.user,)


def choose_invitation_filename(instance, original):
    return "invitations/%s.pdf" % (instance.date.isoformat(),)


class Event(models.Model):
    name = models.CharField(max_length=100,
                            help_text="Názov akcie, napr. Klub Trojstenu "
                            "po Náboji FKS")
    date = models.DateField(unique=True)
    deadline = models.DateTimeField(help_text="Deadline na prihlasovanie")
    invitation = models.FileField(upload_to="invitations", blank=True,
                                  help_text="PDF s pozvánkou, keď bude "
                                  "hotová.")
    sites = models.ManyToManyField(Site)

    class Meta:
        verbose_name = "akcia"
        verbose_name_plural = "akcie"
        ordering = ("-date",)

    def __unicode__(self):
        return "%s %s" % (self.name, self.date.year)

    def get_grouped_lectures(self):
        """
        Returns the lectures for this event in a SortedDict mapping times
        to lists of lectures sorted by their rooms.
        """
        try:
            return self._grouped_lectures_cache
        except AttributeError:
            result = SortedDict()
            for lecture in self.lectures.order_by("time", "room"):
                result.setdefault(lecture.time, []).append(lecture)
            self._grouped_lectures_cache = result
            return result


class Lecture(models.Model):
    event = models.ForeignKey(Event, verbose_name="akcia",
                              related_name="lectures")
    lecturer = models.CharField(max_length=100, verbose_name="prednášajúci")
    title = models.CharField(max_length=147, verbose_name="názov prednášky")
    abstract = models.TextField(blank=True, verbose_name="abstrakt")
    room = models.CharField(max_length=20, verbose_name="miestnosť")
    time = models.TimeField(verbose_name="čas")
    video_url = models.URLField(blank=True, verbose_name="URL videa")

    class Meta:
        verbose_name = "prednáška"
        verbose_name_plural = "prednášky"
        ordering = ("event", "time")

    def __unicode__(self):
        return "%s: %s" % (self.lecturer, self.title)
