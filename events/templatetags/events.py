from __future__ import absolute_import
from django import template

from events import models


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_latest_event(context):
    return models.get_latest_event(context['request'])


@register.simple_tag(takes_context=True)
def active_page_class(context, url):
    request = context['request']
    path = request.path
    if path.startswith('/news/') and url.startswith('/news'):
        return "active"
    if path == url:
        return "active"
    return ""
