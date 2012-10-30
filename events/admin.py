from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from events.models import School, AdditionalUserDetails, Event, Lecture


class AdditionalUserDetailsInline(admin.StackedInline):
    model = AdditionalUserDetails
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (AdditionalUserDetailsInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Event)
admin.site.register(Lecture)
