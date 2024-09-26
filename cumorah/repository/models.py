from django.contrib.contenttypes.models import ContentType
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.documents.models import AbstractDocument
from wagtail.models import Page
from wagtail import fields
from wagtail.documents import get_document_model
from wagtail.documents.models import Document

from cumorah.blocks import standard_cumorah_blocks


DOC_PDF = 'application/pdf'
DOC_EPUB = 'application/epub+zip'
DOC_ZIP = 'application/zip'
DOC_MP3 = 'audio/mpeg'
DOC_MP4 = 'video/mp4'
DOC_TXT = 'text/plain'
DOC_PNG = 'image/png'
DOC_JPG = 'image/jpeg'
DOC_SVG = 'image/svg+xml'

DOC_CHOICES = (
    (DOC_PDF, 'PDF Document'),
    (DOC_EPUB, 'EPUB Book'),
    (DOC_ZIP, 'ZIP Archive'),
    (DOC_MP3, 'MP3 Audio'),
    (DOC_MP4, 'MP4 Video'),
    (DOC_TXT, 'Plain Text'),
    (DOC_PNG, 'PNG Image'),
    (DOC_JPG, 'JPG Image'),
    (DOC_SVG, 'SVG Image'),
)


class CumorahDocument(AbstractDocument):
    content_type = models.CharField(max_length=100, choices=DOC_CHOICES, default=DOC_PDF)

    admin_form_fields = Document.admin_form_fields + (
        'content_type',
    )


class CollectionPage(Page):
    parent_page_types = ['CollectionPage', 'home.HomePage']

    description = fields.StreamField(block_types=standard_cumorah_blocks(), use_json_field=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['child_collections'] = self.get_children().live().filter(content_type=self.content_type)
        doc_content_type = ContentType.objects.get_for_model(DocumentPage)
        context['child_documents'] = self.get_children().live().filter(content_type=doc_content_type)
        return context


class DocumentPage(Page):
    parent_page_types = ['CollectionPage']

    description = fields.StreamField(block_types=standard_cumorah_blocks(), use_json_field=True, null=True)
    document = models.ForeignKey(
        get_document_model(),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    alternate_formats = models.ManyToManyField(
        get_document_model(),
        related_name='document_page_alternates',
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('document'),
        FieldPanel('alternate_formats'),
    ]
