from django.contrib.sites.models import get_current_site


def current_site(request):
    """
    Adds the current site as "site" to the context.
    """
    return {
        'site': get_current_site(request),
    }
