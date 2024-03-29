# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-19 15:10


import cms.models.streamfield
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0019_delete_filter'),
        ('cms', '0016_personindexpage_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='body',
            field=wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock()), (b'affiliation', wagtail.core.blocks.CharBlock(required=False)), (b'style', cms.models.streamfield.PullQuoteStyleChoiceBlock())], icon='openquote')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'link', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'label', wagtail.core.blocks.CharBlock()), (b'style', cms.models.streamfield.LinkStyleChoiceBlock())], icon='link')), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML'))], default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='image',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='wagtailimages.Image'),
            preserve_default=False,
        ),
    ]
