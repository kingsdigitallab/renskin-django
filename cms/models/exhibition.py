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
    InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from django.shortcuts import redirect
from .behaviours import WithFeedImage, WithStreamField, WithOptionalStreamField
from datetime import date
from wagtail.wagtailcore.fields import RichTextField

logger = logging.getLogger(__name__)


class WithThumbnailField(models.Model):

    class Meta:
        abstract = True

    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def get_any_thumbnail(self):
        '''return most relevant thumbnail for a page'''
        ret = self.thumbnail
        return ret


class ExhibitionBasePage(Page, WithOptionalStreamField, WithThumbnailField):

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

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('thumbnail'),
    ]

    def get_context(self, request):
        context = super(ExhibitionBasePage, self).get_context(request)

        # Add extra variables and return the updated context
        import re
        from django.utils.text import slugify

        context['body_classes'] = re.sub(
            r'[A-Z]',
            lambda m: '-' + m.group(0).lower(),
            self.__class__.__name__
        ).strip('-').replace('exhibition-', 'ex-')

        context['body_classes'] += ' ex-' + slugify(self.title)

        return context


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

    def get_feature_pages(self):
        return self.get_children().type(ExhibitionFeaturePage).specific()


class ExhibitionFeaturePage(ExhibitionBasePage, WithStaticMap):
    side_bar_text = RichTextField(blank=True, default='')
    feature_number = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        ordering = ['feature_number']

    content_panels = [
        FieldPanel('feature_number'),
    ] + ExhibitionBasePage.content_panels + [
        # FieldPanel('side_bar_text'),
        InlinePanel('artworks', label='Artworks'),
        # ImageChooserPanel('static_map'),
    ]

    def get_any_thumbnail(self):
        '''return the page thumb, or the first artwork image
        '''
        ret = super(ExhibitionFeaturePage, self).get_any_thumbnail()
        if ret is None:
            artwork = self.artworks.first()
            if artwork:
                ret = artwork.image
        return ret


class Artwork(Orderable):
    feature = ParentalKey(ExhibitionFeaturePage, related_name='artworks')
    title = models.CharField(
        max_length=255, blank=True, default='',
        help_text='The full title of the artwork.'
    )
    dimensions = models.CharField(max_length=255, blank=True, default='')
    credit = models.TextField(blank=True, default='')
    copyright = models.TextField(blank=True, default='')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = '(To specify the HTML alt attribute, click Edit and change the title field.)',
    )

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('dimensions'),
        FieldPanel('credit'),
        FieldPanel('copyright'),
    ]
