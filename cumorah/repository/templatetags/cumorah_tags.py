import logging

from django import template
from django.contrib.contenttypes.models import ContentType

from wagtail.models import Site

from cumorah.repository.models import DocumentPage, CollectionPage

log = logging.getLogger('cumorah')
register = template.Library()


@register.simple_tag(takes_context=True)
def collection_pages(context):
    log.info("%s", context)
    request = context['request']
    try:
        site = Site.find_for_request(request)
    except Site.DoesNotExist:
        log.warning("Can't get current site for collection page links, check sites config.")
        site = Site.objects.all().filter(default=True).first()

    collection = ContentType.objects.get_for_model(CollectionPage)
    qs = site.root_page.get_children().live().filter(content_type=collection, show_in_menus=True)
    return list(qs)
