from django.conf import settings
from django.core import urlresolvers
from django.http import Http404
from django.contrib.flatpages.middleware import FlatpageFallbackMiddleware
from django.contrib.flatpages.views import flatpage


class FlatpageFallbackMiddleware(FlatpageFallbackMiddleware):
    """
    This middleware extends the default FlatpageFallbackMiddleware to
    prevent 404 warnings from getting logged for valid flat pages.
    """
    def process_request(self, request):
        urlconf = getattr(request, 'urlconf', None)
        # Skip if we don't want to append slashes or there's a view for
        # the current URL.
        if (not settings.APPEND_SLASH or
                urlresolvers.is_valid_path(request.path_info, urlconf)):
            return None
        try:
            return flatpage(request, request.path_info)
        except Http404:
            return None
        except:
            if settings.DEBUG:
                raise
            return None
