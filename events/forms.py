# coding: utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from ksp_login.forms import BaseUserProfileForm

from events.models import (AdditionalUserDetails, IndividualSignup,
        IndividualOvernightSignup, SchoolSignup, get_latest_event,
        get_signup_model)


MIN_YEAR = 1900
MAX_YEAR = 3000
MAX_STUDENTS_PER_SCHOOL = 50


class AdditionalUserDetailsForm(BaseUserProfileForm):
    class Meta:
        model = AdditionalUserDetails
        exclude = ('user',)
        widgets = {
            'school': forms.Select(attrs={'class': 'autocomplete'}),
        }

    def clean_graduation(self):
        """
        If the user is a teacher, we allow this to be empty, otherwise
        require the user to provide a value between MIN_YEAR and MAX_YEAR.
        """
        if (self.cleaned_data['is_teacher'] and
                not self.cleaned_data['graduation']):
            return None
        if (not self.cleaned_data['graduation'] or not
                (MIN_YEAR <= self.cleaned_data['graduation'] <= MAX_YEAR)):
            raise forms.ValidationError("Treba zadať valídny rok maturity.")
        return self.cleaned_data['graduation']


class SignupFormMixin(object):
    is_plural = False

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.event = get_latest_event(request)
        self.user = request.user
        super(SignupFormMixin, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(SignupFormMixin, self).save(commit=False)
        if instance.event_id is None:
            instance.event = self.event
        if instance.user_id is None:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class IndividualOvernightSignupFormMixin(SignupFormMixin):
    def clean_sleeping_bag(self):
        if (self.cleaned_data['sleeping_bag'] and not
                self.cleaned_data['sleepover']):
            raise ValidationError("Spacák požičiame iba tým, ktorí "
                                  "prespávajú.")
        return self.cleaned_data['sleeping_bag']

    def clean_sleeping_pad(self):
        if (self.cleaned_data['sleeping_pad'] and not
                self.cleaned_data['sleepover']):
            raise ValidationError("Karimatku požičiame iba tým, ktorí "
                                  "prespávajú.")
        return self.cleaned_data['sleeping_pad']


class SchoolSignupFormMixin(SignupFormMixin):
    is_plural = True

    def clean(self):
        data = self.cleaned_data
        signed_up = sum(data.get('students%d' % (i,), 0) for i in range(1,5))
        if signed_up > MAX_STUDENTS_PER_SCHOOL:
            raise ValidationError("Z jednej školy povoľujeme najviac %d "
                                  "žiakov, %d zadaných." %
                                  (MAX_STUDENTS_PER_SCHOOL, signed_up))
        return super(SchoolSignupFormMixin, self).clean()


signup_form_mixins = {
    IndividualSignup: SignupFormMixin,
    IndividualOvernightSignup: IndividualOvernightSignupFormMixin,
    SchoolSignup: SchoolSignupFormMixin,
}


def get_signup_form(request):
    """
    Returns the appropriate signup form based on the result of
    get_signup_model.
    """
    model_class = get_signup_model(request)
    class SignupForm(signup_form_mixins[model_class], forms.ModelForm):
        class Meta:
            model = model_class
            exclude = ('user', 'event')

    return SignupForm
