# coding: utf-8
from __future__ import unicode_literals
from django.db import models


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

    def __unicode__(self):
        return "%s" % (self.user,)
