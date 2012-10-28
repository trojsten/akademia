# coding: utf-8
from collections import defaultdict
import logging

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic import DateDetailView, DetailView, FormView
from django.views.generic.edit import ModelFormMixin
from django.contrib import messages
from django.contrib.sites.models import get_current_site

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


class AttendanceView(EventDetailView):
    """
    Displays an overview of people attending to a specific event.
    """
    template_name_suffix = '_attendance'

    def get_context_data(self, **kwargs):
        context = super(AttendanceView, self).get_context_data(**kwargs)

        site = get_current_site(self.request)
        overnight_stats = (defaultdict(int)
                           if site.domain == 'klub.trojsten.sk' else None)
        stats = {
            'grades': defaultdict(int),
            'total': 0,
            'lunches': 0,
        }
        seen_school_ids = set()

        school_list = self.object.school_signups.select_related(
                'user__additional_events_details__school')
        preprocessed_schools = []

        for school in school_list:
            seen_school_ids.add(school.user.additional_events_details.school_id)
            stats['lunches'] += school.lunches
            # The +1 is for the teacher.
            stats['total'] += 1
            for grade in range(1, 5):
                students = getattr(school, "students%d" % (grade,))
                stats['grades'][grade] += students
                stats['total'] += students
            preprocessed_schools.append({
                'school': school.user.additional_events_details.school,
                'teacher': school.user,
                'signup': school,
            })

        individual_list = self.object.individual_signups.select_related(
                'user__additional_events_details__school')
        preprocessed_individuals = []

        for individual in individual_list:
            user_details = individual.user.additional_events_details
            grade = user_details.get_grade(self.object.date)
            # If the user's school has a mass signup, don't count this one
            # in the statistics.
            if user_details.school_id not in seen_school_ids:
                # Only count relevant grades.
                if -2 <= grade <= 4:
                    stats['grades'][user_details.get_grade(self.object.date)] += 1
                stats['total'] += 1
                stats['lunches'] += 1
                if overnight_stats is not None:
                    try:
                        signup = individual.individualovernightsignup
                        overnight_stats['oversleeping'] += int(signup.sleepover)
                        overnight_stats['sleeping_pads'] += int(signup.sleeping_pad)
                        overnight_stats['sleeping_bags'] += int(signup.sleeping_bag)
                        overnight_stats['game_participants'] += int(signup.game_participation)
                    except IndividualOvernightSignup.DoesNotExist:
                        logging.warning("Signup %d for user %s and event %s "
                                        "doesn't include overnight info." %
                                        (individual.pk, individual.user,
                                         individual.event), exc_info=True)
            preprocessed_individuals.append({
                'user': individual.user,
                'user_details': user_details,
                'school': user_details.school,
                'grade': grade,
            })

        if overnight_stats is not None:
            stats.update(overnight_stats)

        context.update({
            'school_signups': preprocessed_schools,
            'individual_signups': preprocessed_individuals,
            'signup_stats': stats,
        })

        return context


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
                    messages.success(request, "Úspešne odhlásené z akcie.")
                    return redirect(success_redirect)
            form = form_class(request.POST, instance=signup_instance,
                              request=request)
            if form.is_valid():
                form.save()
                if signup_instance:
                    messages.success(request, "Úspešne zmenená prihláška.")
                else:
                    messages.success(request, "Úspešne prihlásené na akciu.")
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
