from django.views.generic import TemplateView
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import get_current_site

from news.models import Entry


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        site = get_current_site(self.request)
        flatpage = FlatPage.objects.get(sites__id__exact=site.pk,
                                        url="/")
        news = Entry.objects.filter(sites__id__exact=site.pk)[:5]
        return {
            'flatpage': flatpage,
            'news': news,
        }
