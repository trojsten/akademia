from collections import defaultdict

from django.contrib.auth.decorators import (login_required,
    user_passes_test)
from django.contrib.contenttypes.models import ContentType
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from events.models import Event, Lecture
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


class EventPollResultsView(EventDetailView):
    template_name_suffix = '_poll_results'

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super(EventPollResultsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super(EventPollResultsView, self).get_queryset()
        return qs.select_related('poll')

    def get_context_data(self, **kwargs):
        context = kwargs
        context.update(super(EventPollResultsView,
                             self).get_context_data(**kwargs))

        # This follows the structure of EventPollFormSet.__init__ quite
        # closely, maybe they might be generalized somehow?
        event_type = ContentType.objects.get_for_model(Event)
        lecture_type = ContentType.objects.get_for_model(Lecture)
        polls = []
        event = self.object

        if event.poll:
            general_questions = []
            answers = Answer.objects.filter(
                content_type=event_type,
                object_id=event.id,
                question__poll=event.poll
            )
            tmp = defaultdict(list)
            for a in answers:
                tmp[a.question_id].append(a)
            answers = tmp
            questions = Question.objects.filter(poll=event.poll)
            for question in questions:
                processed = self.process_question(question,
                                                  answers[question.id])
                general_questions.append(processed)
            polls.append((EventPollFormSet.general_questions_title,
                          general_questions))

        questions = Question.objects.filter(
            poll__lectures__event=event
        )
        answers = Answer.objects.filter(
            content_type=lecture_type,
            object_id__in=event.lectures.all(),
            # TODO: this might be redundant
            question__in=questions,
        )
        tmp = defaultdict(list)
        for a in answers:
            tmp[(a.question_id, a.object_id)].append(a)
        answers = tmp
        lectures = event.lectures.exclude(poll__isnull=True).select_related('poll').prefetch_related('poll__questions')
        for lecture in lectures:
            lecture_questions = []
            for question in lecture.poll.questions.all():
                processed = self.process_question(question,
                                                  answers[(question.id,
                                                           lecture.id)])
                lecture_questions.append(processed)
            polls.append((lecture, lecture_questions))

        context['polls'] = polls
        return context

    def process_question(self, question, answers):
        result = dict(question=question)
        if question.type == Question.TEXT:
            result['answers'] = answers
        else:
            distribution = defaultdict(int)
            for a in answers:
                distribution[a.value] += 1
            counts = [(text, distribution[str(num)])
                      for num, text in Answer.STARS_CHOICES]
            if sum(count for _, count in counts):
                result['options'] = counts
            # TODO: add statistics (average, mean, deviation, ...)

        return result
