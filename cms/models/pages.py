

import logging

from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from django.shortcuts import redirect
from .behaviours import WithFeedImage, WithStreamField
from datetime import date

logger = logging.getLogger(__name__)


def _paginate(request, items):
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(items, settings.ITEMS_PER_PAGE)

    try:
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        items = paginator.page(1)

    return items


class PersonIndexPage(Page, WithStreamField):
    subpage_types = ['Person', ]


PersonIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),

]

PersonIndexPage.promote_panels = Page.promote_panels


class Person(Page, WithStreamField):
    search_fields = Page.search_fields + [
    ]
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True
    )
    subpage_types = ['ImagePage', ]


Person.content_panels = [
    FieldPanel('title', classname='full title'),
    ImageChooserPanel('image'),
    StreamFieldPanel('body'),
]

Person.promote_panels = Page.promote_panels


class ChapterIndexPage(Page):
    subpage_types = ['Chapter', ]


ChapterIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
]

ChapterIndexPage.promote_panels = Page.promote_panels


class Chapter(RoutablePageMixin, Page):
    search_fields = Page.search_fields + [
    ]

    subpage_types = ['ImagePage', ]

    @route(r'^(?P<slug>[\w\- ]+)/$')
    def view_func(self, request, slug=None):
        image_page = ImagePage.objects.get(slug=slug)
        return redirect('{}#image_thumb{}'.format(
            self.get_url(), image_page.id)
        )


Chapter.content_panels = [
    FieldPanel('title', classname='full title'),
]

Chapter.promote_panels = Page.promote_panels


class ImagePage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True
    )
    subpage_types = []


ImagePage.content_panels = [
    FieldPanel('title', classname='full title'),
    ImageChooserPanel('image'),
    StreamFieldPanel('body'),
]

ImagePage.promote_panels = Page.promote_panels


class HomePage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = [
        'BlogIndexPage', 'EventIndexPage', 'IndexPage',
        'NewsIndexPage', 'PastEventIndexPage', 'RichTextPage',
        'ChapterIndexPage', 'PersonIndexPage', 'ExhibitionHomePage'
    ]

    def get_chapters(self):
        return Chapter.objects.live()

    def get_events(self):
        # Events that have not ended.
        today = date.today()
        events = Event.objects.live().filter(date_from__gte=today).order_by(
            'date_from')[:2]
        return events

    def get_news(self):
        news = NewsPost.objects.live().order_by('-date')[:2]
        return news


HomePage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

HomePage.promote_panels = Page.promote_panels


class IndexPage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['IndexPage', 'RichTextPage']


IndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

IndexPage.promote_panels = Page.promote_panels


class RichTextPage(Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = []


RichTextPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

RichTextPage.promote_panels = Page.promote_panels


class BlogIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['BlogPost']

    @property
    def posts(self):
        posts = BlogPost.objects.live().descendant_of(self)

        posts = posts.order_by('-date')

        return posts

    @route(r'^$')
    def all_posts(self, request):
        posts = self.posts

        return render(request, self.get_template(request),
                      {'self': self, 'posts': _paginate(request, posts)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )


BlogIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

BlogIndexPage.promote_panels = Page.promote_panels


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey('BlogPost', related_name='tagged_items')


class BlogPost(Page, WithStreamField, WithFeedImage):
    date = models.DateField()
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('date'),
        index.RelatedFields('tags', [
                            index.SearchField('name'),
                            index.SearchField('slug'),
                            ]),
    ]

    subpage_types = []

    def get_index_page(self):
        # Find closest ancestor which is a blog index
        return BlogIndexPage.objects.ancestor_of(self).last()


BlogPost.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    StreamFieldPanel('body'),
]

BlogPost.promote_panels = Page.promote_panels + [
    FieldPanel('tags'),
    ImageChooserPanel('feed_image'),
]


# News pages
class NewsIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['NewsPost']

    @property
    def posts(self):
        posts = NewsPost.objects.live().descendant_of(self)

        posts = posts.order_by('-date')

        return posts

    @route(r'^$')
    def all_posts(self, request):
        posts = self.posts

        return render(request, self.get_template(request),
                      {'self': self, 'posts': _paginate(request, posts)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'posts': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )


NewsIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

NewsIndexPage.promote_panels = Page.promote_panels


class NewsPostTag(TaggedItemBase):
    content_object = ParentalKey('NewsPost', related_name='tagged_items')


class NewsPost(Page, WithStreamField, WithFeedImage):

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True
    )

    date = models.DateField()
    tags = ClusterTaggableManager(through=NewsPostTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('date'),
        index.RelatedFields('tags', [
                            index.SearchField('name'),
                            index.SearchField('slug'),
                            ]),
    ]

    subpage_types = []

    def get_index_page(self):
        # Find closest ancestor which is a news index
        return NewsIndexPage.objects.ancestor_of(self).last()


NewsPost.content_panels = [
    FieldPanel('title', classname='full title'),
    ImageChooserPanel('image'),
    FieldPanel('date'),
    StreamFieldPanel('body'),
]

NewsPost.promote_panels = Page.promote_panels + [
    FieldPanel('tags'),
    ImageChooserPanel('feed_image'),
]


class EventIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = ['Event', 'PastEventIndexPage', 'AllEventIndexPage']

    @property
    def events(self):
        # Events that have not ended.
        # today = date.today()
        # events = Event.objects.live().filter(date_from__gte=today).order_by(
        #     'date_from')
        # GN: ALL events
        events = Event.objects.live().order_by('-date_from')
        return events

    @route(r'^$')
    def all_events(self, request):
        events = self.events

        return render(request, self.get_template(request),
                      {'self': self, 'events': _paginate(request, events)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'events': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )


EventIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

EventIndexPage.promote_panels = Page.promote_panels


class PastEventIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = []

    @property
    def events(self):
        # Events that have not ended.
        today = date.today()
        events = Event.objects.live().filter(date_from__lt=today).order_by(
            '-date_from')
        return events

    @route(r'^$')
    def all_events(self, request):
        events = self.events
        return render(request, self.get_template(request),
                      {'self': self, 'events': _paginate(request, events)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'events': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )


class AllEventIndexPage(RoutablePageMixin, Page, WithStreamField):
    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    subpage_types = []

    @property
    def events(self):
        events = Event.objects.live().order_by('-date_from')
        return events

    @route(r'^$')
    def all_events(self, request):
        events = self.events
        return render(request, self.get_template(request),
                      {'self': self, 'events': _paginate(request, events)})

    @route(r'^tag/(?P<tag>[\w\- ]+)/$')
    def tag(self, request, tag=None):
        if not tag:
            # Invalid tag filter
            logger.error('Invalid tag filter')
            return self.all_posts(request)

        posts = self.posts.filter(tags__name=tag)

        return render(
            request, self.get_template(request), {
                'self': self, 'events': _paginate(request, posts),
                'filter_type': 'tag', 'filter': tag
            }
        )

PastEventIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    StreamFieldPanel('body'),
]

PastEventIndexPage.promote_panels = Page.promote_panels


class EventTag(TaggedItemBase):
    content_object = ParentalKey('Event', related_name='tagged_items')


class Event(Page, WithStreamField, WithFeedImage):

    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True
    )
    date_from = models.DateField(verbose_name="Start Date")
    date_to = models.DateField(verbose_name="End Date (Leave blank if\
                               not required)", blank=True, null=True)
    time = models.TimeField(verbose_name="Time of Event")
    time_end = models.TimeField(verbose_name="End Time (leave blank if\
                                not required)", blank=True, null=True)

    location = models.TextField(verbose_name="Location")

    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('date_from'),
        index.SearchField('date_to'),
        index.RelatedFields('tags', [
                            index.SearchField('name'),
                            index.SearchField('slug'),
                            ]),
    ]

    subpage_types = []

    def get_index_page(self):
        # Find closest ancestor which is a blog index
        return EventIndexPage.objects.ancestor_of(self).last()


Event.content_panels = [
    FieldPanel('title', classname='full title'),

    ImageChooserPanel('image'),
    FieldPanel('date_from'),
    FieldPanel('date_to'),
    FieldPanel('time'),
    FieldPanel('time_end'),
    FieldPanel('location'),

    StreamFieldPanel('body'),
]

Event.promote_panels = Page.promote_panels + [
    FieldPanel('tags'),
]
