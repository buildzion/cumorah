
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks


def standard_cumorah_blocks(*extra_blocks):
    standard_blocks = [
        ('heading', blocks.CharBlock(form_classname='title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('document', DocumentChooserBlock()),
    ]

    standard_blocks.extend(extra_blocks)
    return standard_blocks
