# Generated by Django 4.2.16 on 2024-09-25 04:21

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('document', wagtail.documents.blocks.DocumentChooserBlock())], null=True, use_json_field=True)),
                ('alternate_formats', models.ManyToManyField(related_name='document_page_alternates', to='repository.cumorahdocument')),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='repository.cumorahdocument')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='singledocumentpage',
            name='document',
        ),
        migrations.RemoveField(
            model_name='singledocumentpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='MultipleDocumentPage',
        ),
        migrations.DeleteModel(
            name='SingleDocumentPage',
        ),
    ]
