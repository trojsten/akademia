from django import forms
from django.dispatch import receiver
from ksp_login.signals import user_form_requested

from events.models import AdditionalUserDetails


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
