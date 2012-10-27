from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic import DateDetailView, DetailView, FormView
from django.views.generic.edit import ModelFormMixin
from django.contrib.sites.models import get_current_site

from events.decorators import class_view_decorator
from events.forms import get_signup_form
from events.models import Event, get_latest_event, get_signup_model


class EventDetailView(DateDetailView):
    allow_future = True
    date_field = "date"
    month_format = '%m'
    model = Event
    context_object_name = 'event'
    # This is a hack to prevent SingleObjectMixin.get_object from
    # complaining since in our case the date is unique and sufficient.
    slug_field = 'name__contains'

    def get_queryset(self):
        return self.model.objects.filter(
            sites__id__exact=get_current_site(self.request).pk
        )


def latest_event_detail(request, success_redirect='event_latest'):
    """
    Shows the defails of the latest event same as EventDetailView. In
    addition checks whether the signup period is still open and if it is,
    handles the appropriate signup form as well.
    """
    event = get_latest_event(request)
    if request.user.is_authenticated():
        form_class = get_signup_form(request)
        signup_model = get_signup_model(request)
        try:
            signup_instance = signup_model.objects.get(
                user=request.user,
                event=event,
            )
        except signup_model.DoesNotExist:
            signup_instance = None

    context = {
        'event': event,
    }

    if request.user.is_authenticated():
        if request.method == 'POST' and event.signup_period_open():
            if 'sign_out' in request.POST:
                # Sign the user out of the event. If they aren't signed up, do
                # nothing.
                if signup_instance:
                    signup_instance.delete()
                    # TODO: add a message
                    return redirect(success_redirect)
            form = form_class(request.POST, instance=signup_instance,
                              request=request)
            if form.is_valid():
                form.save()
                return redirect(success_redirect)
        else:
            form = form_class(instance=signup_instance, request=request)

        context.update({
            'signup_form': form,
            'is_signed_up': signup_instance is not None,
        })

    return TemplateResponse(request=request,
                            template='events/event_detail.html',
                            context=context)
