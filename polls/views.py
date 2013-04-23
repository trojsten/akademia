from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from events.views import EventDetailView
from polls.models import Answer, Poll, Question
from polls.forms import EventPollFormSet


class EventPollView(FormView, EventDetailView):
    form_class = EventPollFormSet
    template_name = 'events/event_poll.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventPollView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(EventPollView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = kwargs
        context.update(EventDetailView.get_context_data(self, **context))
        context['polls'] = context['form'].forms
        return context

    def get_form_kwargs(self):
        self.object = self.get_object()
        kwargs = super(EventPollView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'event': self.object,
        })
        return kwargs

    def get_queryset(self):
        qs = super(EventPollView, self).get_queryset()
        return qs.select_related('poll')

    def get_success_url(self):
        return ""
