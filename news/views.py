from django.views.generic import ListView

from news.models import Entry


class EntryListView(ListView):
    model = Entry
    template_name = 'news/index.html'
    context_object_name = 'news_entries'
    paginate_by = 10
