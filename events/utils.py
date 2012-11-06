"""
This module provides functions taken from future releases of Django.
Currently it contains the slugify function.
"""

try:
    from django.utils.text import slugify
except ImportError:
    import re
    import unicodedata
    from django.utils.functional import allow_lazy
    from django.utils.safestring import mark_safe
    def slugify(value):
        """
        Converts to lowercase, removes non-word characters (alphanumerics and
        underscores) and converts spaces to hyphens. Also strips leading and
        trailing whitespace.
        """
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return mark_safe(re.sub('[-\s]+', '-', value))
    slugify = allow_lazy(slugify, unicode)
