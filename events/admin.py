from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from events.models import (School, AdditionalUserDetails, Event, Lecture,
        IndividualSignup, IndividualOvernightSignup, SchoolSignup)


class AdditionalUserDetailsInline(admin.StackedInline):
    model = AdditionalUserDetails
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (AdditionalUserDetailsInline,)
admin.site.unregister(User)


class LectureInline(admin.StackedInline):
    model = Lecture
    extra = 0


class SignupInline(object):
    """
    This class is here just to make all signup inlines have a common base.
    """
    pass


class IndividualSignupInline(SignupInline, admin.TabularInline):
    model = IndividualSignup
    extra = 0


class IndividualOvernightSignupInline(SignupInline, admin.TabularInline):
    model = IndividualOvernightSignup
    extra = 0


class SchoolSignupInline(SignupInline, admin.TabularInline):
    model = SchoolSignup
    extra = 0


class EventAdmin(admin.ModelAdmin):
    model = Event
    inlines = (LectureInline, IndividualSignupInline,
               IndividualOvernightSignupInline, SchoolSignupInline)

    def get_inline_instances(self, request, obj=None):
        if obj is not None:
            klub = obj.sites.filter(domain__exact='klub.trojsten.sk').count() > 0
        inline_instances = []
        for inline_class in self.inlines:
            if issubclass(inline_class, SignupInline):
                if obj is None:
                    # Omit all signup inlines when creating a new event.
                    continue
                if klub and inline_class is not IndividualOvernightSignupInline:
                    continue
                elif not klub and inline_class is IndividualOvernightSignupInline:
                    continue
            inline = inline_class(self.model, self.admin_site)
            if request:
                if not (inline.has_add_permission(request) or
                        inline.has_change_permission(request, obj) or
                        inline.has_delete_permission(request, obj)):
                    continue
                if not inline.has_add_permission(request):
                    inline.max_num = 0
            inline_instances.append(inline)

        return inline_instances


admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Event, EventAdmin)
admin.site.register(Lecture)
