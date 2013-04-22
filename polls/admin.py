from django.contrib import admin

from polls.models import Poll, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class PollAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)


admin.site.register(Poll, PollAdmin)
