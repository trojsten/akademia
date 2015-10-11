from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown as markdown_module

register = template.Library()

@register.filter(name='markdown')
@stringfilter
def markdown(value, arg=None):
    """
    Filter to create HTML out of Markdown, using custom extensions.

    Usage::

        {{ object.text|markdown }}
        {{ object.text|markdown:"safe" }}
        {{ object.text|markdown:"codehilite" }}
        {{ object.text|markdown:"safe,codehilite" }}

    Inspired by
    http://programanddesign.com/uncategorized/django-flatpages-markdown-and-syntax-highlighting/
    """
    extensions = []
    safe_mode = False
    if arg is not None:
        extensions = {"markdown.extensions.{}".format(ext) for ext in arg.split(",")}
    if "safe" in extensions:
        extensions.pop("safe")
        safe_mode = True
    return mark_safe(markdown_module.markdown(value, extensions=extensions,
                                              safe_mode=safe_mode))
