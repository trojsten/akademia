from django.contrib import admin

from polls.models import Poll, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class PollAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.9.1/jquery-ui.min.js',
            'js/admin-ordering.js',
        )


admin.site.register(Poll, PollAdmin)
