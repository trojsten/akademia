# coding: utf-8
from __future__ import unicode_literals


def __monkeypatch_flatpage():
    from django.contrib.flatpages.models import FlatPage

    field = FlatPage._meta.get_field('content')
    field.help_text = ('Obsah bude renderovaný <a '
                       'href="http://en.wikipedia.org/wiki/Markdown">'
                       'Markdownom</a>.')

__monkeypatch_flatpage()
del __monkeypatch_flatpage
