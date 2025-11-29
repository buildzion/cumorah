from django.conf import settings
from django.utils.safestring import mark_safe


def site_settings(request):
    return {
        "cumorah_stylesheets": settings.CUMORAH_STYLESHEETS,
        "cumorah_javascript": settings.CUMORAH_JAVASCRIPT,
        "cumorah_navbar_title": mark_safe(settings.CUMORAH_NAVBAR_TITLE),
    }
