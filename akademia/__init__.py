# coding: utf-8
from __future__ import unicode_literals


def __monkeypatch_flatpage():
    # Add a help_text to flatpages context.
    from django.contrib.flatpages.models import FlatPage

    field = FlatPage._meta.get_field('content')
    field.help_text = ('Obsah bude renderovaný <a '
                       'href="http://en.wikipedia.org/wiki/Markdown">'
                       'Markdownom</a>.')

    # Fix an exception on save when no sites are selected.
    from django.contrib.flatpages.forms import FlatpageForm

    def clean(self):
        url = self.cleaned_data.get('url', None)
        sites = self.cleaned_data.get('sites', None)

        same_url = FlatPage.objects.filter(url=url)
        if self.instance.pk:
            same_url = same_url.exclude(pk=self.instance.pk)

        if sites and same_url.filter(sites__in=sites).exists():
            for site in sites:
                if same_url.filter(sites=site).exists():
                    raise forms.ValidationError(
                        _('Flatpage with url %(url)s already exists for site %(site)s' %
                          {'url': url, 'site': site}))

        return super(FlatpageForm, self).clean()

    FlatpageForm.clean = clean

__monkeypatch_flatpage()
del __monkeypatch_flatpage
