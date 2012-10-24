from django.conf.urls import patterns, include, url

from events.views import EventDetailView, LastEventDetailView


urlpatterns = patterns("",
    url(r'^$', LastEventDetailView.as_view(), name="event_latest"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        EventDetailView.as_view(), kwargs={'slug': ''},
        name="event_detail"),
)
