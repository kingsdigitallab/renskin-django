# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 11:47


import cms.models.streamfield
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('wagtailimages', '0018_remove_rendition_filter'),
        ('cms', '0004_update_field_body_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([(b'home', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'title', wagtail.core.blocks.CharBlock()), (b'description', wagtail.core.blocks.RichTextBlock())], icon='grip', label='Homepage Block')), (b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock()), (b'affiliation', wagtail.core.blocks.CharBlock(required=False)), (b'style', cms.models.streamfield.PullQuoteStyleChoiceBlock())], icon='openquote')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'link', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'label', wagtail.core.blocks.CharBlock()), (b'style', cms.models.streamfield.LinkStyleChoiceBlock())], icon='link')), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML'))])),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([(b'home', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'title', wagtail.core.blocks.CharBlock()), (b'description', wagtail.core.blocks.RichTextBlock())], icon='grip', label='Homepage Block')), (b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h5', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock()), (b'affiliation', wagtail.core.blocks.CharBlock(required=False)), (b'style', cms.models.streamfield.PullQuoteStyleChoiceBlock())], icon='openquote')), (b'image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'link', wagtail.core.blocks.StructBlock([(b'url', wagtail.core.blocks.URLBlock(required=False)), (b'page', wagtail.core.blocks.PageChooserBlock(required=False)), (b'label', wagtail.core.blocks.CharBlock()), (b'style', cms.models.streamfield.LinkStyleChoiceBlock())], icon='link')), (b'embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), (b'html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML'))])),
                ('date', models.DateField()),
                ('feed_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='NewsPostTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='cms.NewsPost')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cms_newsposttag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newspost',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='cms.NewsPostTag', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
