# coding: utf-8
from django import forms
from django.dispatch import receiver
from ksp_login.signals import user_form_requested

from events.models import AdditionalUserDetails


MIN_YEAR = 1900
MAX_YEAR = 3000


class AdditionalUserDetailsForm(forms.ModelForm):
    class Meta:
        model = AdditionalUserDetails
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        kwargs.pop('request', None)
        user = kwargs.pop('user', None)
        self.user = user
        if user is not None:
            instance, created = AdditionalUserDetails.objects.get_or_create(user=user)
            kwargs['instance'] = instance
        super(AdditionalUserDetailsForm, self).__init__(*args, **kwargs)

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

    def set_user(self, user):
        self.user = user

    def save(self, commit=True):
        instance = super(AdditionalUserDetailsForm, self).save(commit=False)
        if self.user is not None:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


@receiver(user_form_requested, dispatch_uid='additional details form')
def register_additional_user_details_form(sender, **kwargs):
    return AdditionalUserDetailsForm
