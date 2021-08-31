from __future__ import unicode_literals

import logging
import re
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel, \
    InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from .behaviours import WithFeedImage, WithStreamField, WithOptionalStreamField
from wagtail.wagtailcore.fields import RichTextField
from django.conf import settings

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

        context['visible_skin_page'] = Page.objects.get(slug=settings.VISIBLE_SKIN_SLUG)

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

    def get_other_pages(self):
        return self.get_children().not_type(ExhibitionFeaturePage).specific()


class ExhibitionFeaturePage(ExhibitionBasePage, WithStaticMap):
    side_bar_text = RichTextField(blank=True, default='')
    feature_number = models.IntegerField(
        blank=True, null=True, default=None,
        help_text='This number should match the one used in the physical exhibition and the map.'
    )

    class Meta:
        ordering = ['feature_number']

    content_panels = [
        FieldPanel('feature_number'),
        InlinePanel('artworks', label='Artworks'),
    ] + ExhibitionBasePage.content_panels[1:] + [
        ImageChooserPanel('static_map'),
    ]

    promote_panels = ExhibitionBasePage.promote_panels + [
        FieldPanel('title'),
    ]
    
    def full_clean(self, *args, **kwargs):
        self.title = self.short_title
        super(ExhibitionFeaturePage, self).full_clean(*args, **kwargs)

    def get_admin_display_title(self):
        return '{:02d} - {}'.format(self.feature_number, self.title)

    def get_any_thumbnail(self):
        '''return the page thumb, or the first artwork image
        '''
        ret = super(ExhibitionFeaturePage, self).get_any_thumbnail()
        if ret is None:
            artwork = self.artworks.first()
            if artwork:
                ret = artwork.image
        return ret

    def get_artwork_reworked(self):
        ret = self.artworks.first()
        return ret

    reworked = property(get_artwork_reworked)

    def get_artwork_original(self):
        ret = self.artworks.last()
        return ret

    original = property(get_artwork_original)

    '''
    Conventions:
    long_title = 'short_title: sub_title'
    long_title comes from first artwork's title
    '''

    def _get_title_parts(self):
        '''Return [short_title, subtitle]'''
        long_title = self.long_title
        match = re.match(r'^(.*?)([,.;:-])(.*)$', long_title)
        if match:
            ret = [match.group(1).strip(), match.group(3).strip()]
        else:
            ret = [long_title, '']

        return ret

    def get_short_title(self):
        return self._get_title_parts()[0]

    short_title = property(get_short_title)

    def get_subtitle(self):
        return self._get_title_parts()[1]

    subtitle = property(get_subtitle)

    def get_long_title(self):
        ret = self.title
        reworked = self.reworked
        if reworked:
            ret = reworked.title

        return (ret or '').strip()

    long_title = property(get_long_title)


class Artwork(Orderable):
    feature = ParentalKey(ExhibitionFeaturePage, related_name='artworks')
    title = models.CharField(
        max_length=255, blank=True, default='',
        help_text='The complete title of the artwork. Without author name, date or any other information.'
    )
    dimensions = models.CharField(max_length=255, blank=True, default='')
    credit = models.TextField('Credit line',
        blank=True, default='',
        help_text = "e.g. Chistoph Weiditz, TITLE, 1529, Germanisches National Museum. TITLE will be substituted by the title field."
    )
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
        # FieldPanel('dimensions'),
        FieldPanel('credit'),
        # FieldPanel('copyright'),
    ]

    def get_credit_line(self):
        return (self.credit or '').replace('TITLE', "'{}'".format(self.title))

    credit_line = property(get_credit_line)
