from __future__ import unicode_literals

import logging

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, \
    InlinePanel
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from django.shortcuts import redirect
from .behaviours import WithFeedImage, WithStreamField, WithOptionalStreamField
from datetime import date
from wagtail.wagtailcore.fields import RichTextField

logger = logging.getLogger(__name__)


class ExhibitionBasePage(Page, WithOptionalStreamField):
    class Meta:
        abstract = True

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    # subpage_types = ['ExhibitionBasePage', 'ExhibitionSubPage', 'IndexPage']

    content_panels = Page.content_panels + [
        # FieldPanel('title', classname='full title'),
        StreamFieldPanel('body'),
    ]


class WithStaticMap(models.Model):
    class Meta:
        abstract = True

    static_map = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )


class ExhibitionHomePage(ExhibitionBasePage, WithStaticMap):

    # intro = RichTextField()
    dates_times = RichTextField(blank=True, default='')
    locations = RichTextField(blank=True, default='')
    # biography = RichTextField()

    content_panels = ExhibitionBasePage.content_panels + [
        FieldPanel('dates_times'),
        FieldPanel('locations'),
    ]


class ExhibitionPage(ExhibitionBasePage):
    pass


class ExhibitionGalleryPage(ExhibitionBasePage):
    pass


class ExhibitionFeaturePage(ExhibitionBasePage, WithStaticMap):

    side_bar_text = RichTextField(blank=True, default='')

    content_panels = ExhibitionBasePage.content_panels + [
        FieldPanel('side_bar_text'),
        InlinePanel('artworks', label='Artworks'),
        ImageChooserPanel('static_map'),
    ]


class Artwork(Orderable):
    feature = ParentalKey(ExhibitionFeaturePage, related_name='artworks')
    title = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255, blank=True, default='')
    credit = models.TextField(blank=True, default='')
    copyright = models.TextField(blank=True, default='')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('dimensions'),
        FieldPanel('credit'),
        FieldPanel('copyright'),
        ImageChooserPanel('image'),
    ]
