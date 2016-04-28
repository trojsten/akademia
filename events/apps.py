from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = 'events'

    def ready(self):
        # Force an import of forms to register AdditionalUserDetailsForm
        # with the user_form_requested signal.
        from events import forms
