from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from events.models import (School, AdditionalUserDetails, Event, Lecture,
        IndividualSignup, IndividualOvernightSignup, SchoolSignup)

# The following series of imports is there just to support the overridden
# EventAdmin.change_view.
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db import models, transaction, router
from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects, model_format_dict
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_unicode
from django.utils.html import escape, escapejs
from django.core.urlresolvers import reverse
from django.forms.formsets import all_valid
from django.contrib.admin import widgets, helpers
from django.utils.translation import ugettext as _

csrf_protect_m = method_decorator(csrf_protect)
# This ends here.


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

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """The 'change' admin view for this model.

        Taken verbatim from the sources of 1.4 and adds the 'obj' argument
        to get_inline_instances.
        """
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and "_saveasnew" in request.POST:
            return self.add_view(request, form_url=reverse('admin:%s_%s_add' %
                                    (opts.app_label, opts.module_name),
                                    current_app=self.admin_site.name))

        ModelForm = self.get_form(request, obj)
        formsets = []
        inline_instances = self.get_inline_instances(request, obj)
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, new_object), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object, prefix=prefix,
                                  queryset=inline.queryset(request))

                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, True)
                self.save_related(request, form, formsets, True)
                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            form = ModelForm(instance=obj)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, obj), inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1 or not prefix:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
            self.get_prepopulated_fields(request, obj),
            self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            prepopulated = dict(inline.get_prepopulated_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, prepopulated, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': "_popup" in request.REQUEST,
            'media': media,
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj, form_url=form_url)

    def get_formsets(self, request, obj=None):
        """
        Taken from 1.5; adds the obj parameter to get_inline_instances.
        """
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

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
