from django.contrib.sites.shortcuts import get_current_site


def current_site(request):
    """
    Adds the current site as "site" to the context.
    """
    return {
        'site': get_current_site(request),
    }
