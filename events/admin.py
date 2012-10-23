from django.contrib import admin

from events.models import School, AdditionalUserDetails, Event, Lecture


admin.site.register(School)
admin.site.register(AdditionalUserDetails)
admin.site.register(Event)
admin.site.register(Lecture)
