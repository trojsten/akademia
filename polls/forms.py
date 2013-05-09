# coding: utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.contenttypes.models import ContentType

from events.models import Lecture
from polls.models import Answer, Poll, Question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('value',)

    def save(self, *args, **kwargs):
        # FIXME: all wrong, need to delete in case an instance exists and
        # is cleared
        if self.cleaned_data['value']:
            return super(AnswerForm, self).save(*args, **kwargs)
        return None


class StarsAnswerForm(AnswerForm):
    OPTIONAL_STARS_CHOICES = (('', 'žiadna odpoveď'),) + Answer.STARS_CHOICES
    value = forms.ChoiceField(choices=OPTIONAL_STARS_CHOICES,
                              required=False,
                              widget=forms.RadioSelect(attrs={
                                  'class': 'stars',
                              }))

    class Meta(AnswerForm.Meta):
        pass


forms_for_answer_types = {
    Question.TEXT: AnswerForm,
    Question.STARS: StarsAnswerForm,
}


def answer_form_factory(question, **kwargs):
    form_class = forms_for_answer_types[question.type]
    return form_class(**kwargs)


class EventPollFormSet(object):
    """
    This class glues together the whole questionnaire for a single event
    into a single object which mimics the behavior of a form. It is used
    as the form in EventPollView which is a descendant of FormWiew.
    """
    general_questions_title = "Všeobecné otázky"
    form_prefix = "%(target_type)s_%(target_id)s_%(question_id)s"

    def __init__(self, request, event, **form_kwargs):
        """
        This sets up all required AnswerForm instances in self.form with
        the appropriate prefixes.
        """
        # TODO: there is some nontrivial code duplication in here, factor
        # it out
        event_type = ContentType.objects.get_for_model(event)
        lecture_type = ContentType.objects.get_for_model(Lecture)
        forms = []
        self.forms = forms

        if event.poll:
            general_forms = []
            answers = Answer.objects.filter(
                user=request.user,
                content_type=event_type,
                object_id=event.id,
                question__poll=event.poll
            )
            answers = dict((a.question_id, a) for a in answers)
            questions = Question.objects.filter(poll=event.poll)
            for question in questions:
                defaults = {
                    'question': question,
                    'user': request.user,
                    'target': event,
                }
                instance = answers.get(question.id) or Answer(**defaults)
                prefix = self.form_prefix % {
                    'target_type': event_type,
                    'target_id': event.id,
                    'question_id': question.id,
                }
                form = answer_form_factory(question, instance=instance,
                                           prefix=prefix, **form_kwargs)
                general_forms.append((question, form))

            forms.append((self.general_questions_title, general_forms))

        questions = Question.objects.filter(
            poll__lectures__event=event
        )
        answers = Answer.objects.filter(
            user=request.user,
            content_type=lecture_type,
            object_id__in=event.lectures.all(),
            # TODO: this might be redundant
            question__in=questions,
        )
        answers = dict(((a.question_id, a.object_id), a) for a in answers)
        lectures = event.lectures.exclude(poll__isnull=True).select_related('poll').prefetch_related('poll__questions')
        for lecture in lectures:
            lecture_forms = []
            for question in lecture.poll.questions.all():
                defaults = {
                    'question': question,
                    'user': request.user,
                    'target': lecture,
                }
                instance = (answers.get((question.id, lecture.id)) or
                            Answer(**defaults))
                prefix = self.form_prefix % {
                    'target_type': lecture_type,
                    'target_id': lecture.id,
                    'question_id': question.id,
                }
                form = answer_form_factory(question, instance=instance,
                                           prefix=prefix, **form_kwargs)
                lecture_forms.append((question, form))

            forms.append((lecture, lecture_forms))

    def is_valid(self):
        return all(form.is_valid()
                   for title, group in self.forms
                   for question, form in group)

    def save(self, commit=True):
        instances = [form.save(commit)
                     for title, group in self.forms
                     for question, form in group]
        return [i for i in instances if i is not None]
