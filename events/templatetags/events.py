from __future__ import absolute_import
from django import template

from events import models


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_latest_event(context):
    return models.get_latest_event(context['request'])
