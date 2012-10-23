# coding: utf-8
from __future__ import unicode_literals
from django.db import models


class School(models.Model):
    abbreviation = models.CharField(max_length=23,
                                    verbose_name="skratka",
                                    help_text="Sktatka názvu školy.")
    verbose_name = models.CharField(max_length=47,
                                    verbose_name="celý názov")
    addr_name = models.CharField(max_length=47)
    street = models.CharField(max_length=47)
    city = models.CharField(max_length=47)
    zip_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "škola"
        verbose_name_plural = "školy"
        ordering = ("verbose_name",)

    def __unicode__(self):
        return self.verbose_name
