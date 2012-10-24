from django.views.generic import DateDetailView, DetailView
from events.models import Event


class EventDetailMixin(object):
    model = Event
    context_object_name = 'event'

class EventDetailView(EventDetailMixin, DateDetailView):
    allow_future = True
    date_field = "date"
    month_format = '%m'
    # This is a hack to prevent SingleObjectMixin.get_object from
    # complaining since in our case the date is unique and sufficient.
    slug_field = 'name__contains'


class LastEventDetailView(EventDetailMixin, DetailView):
    def get_object(self):
        return self.model.objects.order_by('-date')[0]
