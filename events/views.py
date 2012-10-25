from django.views.generic import DateDetailView, DetailView
from django.contrib.sites.models import get_current_site
from events.models import Event


class EventDetailMixin(object):
    model = Event
    context_object_name = 'event'

    def get_queryset(self):
        return self.model.objects.filter(
            sites__id__exact=get_current_site(self.request).pk
        )

class EventDetailView(EventDetailMixin, DateDetailView):
    allow_future = True
    date_field = "date"
    month_format = '%m'
    # This is a hack to prevent SingleObjectMixin.get_object from
    # complaining since in our case the date is unique and sufficient.
    slug_field = 'name__contains'


class LastEventDetailView(EventDetailMixin, DetailView):
    def get_object(self):
        return self.get_queryset().order_by('-date')[0]
