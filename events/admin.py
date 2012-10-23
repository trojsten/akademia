from django.contrib import admin

from events.models import School, AdditionalUserDetails


admin.site.register(School)
admin.site.register(AdditionalUserDetails)
