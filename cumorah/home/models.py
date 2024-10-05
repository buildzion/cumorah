from django.db import models
from wagtail.admin.panels import FieldPanel

from wagtail.models import Page
from wagtail import fields
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from cumorah.blocks import standard_cumorah_blocks


class HomePage(Page):
    subpage_types = ['repository.CollectionPage', 'HomePage']
    # parent_page_types = ['home.HomePage']

    body = fields.StreamField(block_types=standard_cumorah_blocks(), use_json_field=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


class MenuLink(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='+')
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    panels = [
        FieldPanel('page'),
        FieldPanel('order'),
        FieldPanel('active'),
    ]

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.page.__str__()


class MenuLinkViewSet(SnippetViewSet):
    model = MenuLink
    list_display = ('page', 'order', 'active')

register_snippet(MenuLinkViewSet)
