import re

from django import template
from django.conf import settings

from cms.models.pages import BlogPost, Event, NewsPost
from datetime import date

register = template.Library()

# <h1 class="NOT_IN_TOC"> => ignored by the toc tag
NOT_IN_TOC = 'not-in-toc'


@register.filter
def next(some_list, current_index):
    """
    Returns the next element of the list using the current index if it exists.
    Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) + 1]  # access the next element
    except:
        return ''  # return empty string in case of exception


@register.filter
def previous(some_list, current_index):
    """
    Returns the previous element of the list using the current
    index if it exists. Otherwise returns an empty string.
    """
    try:
        return some_list[int(current_index) - 1]  # access the previous element
    except:
        return ''  # return empty string in case of exception


@register.simple_tag
def are_comments_allowed():
    """Returns True if commenting on the site is allowed, False otherwise."""
    return getattr(settings, 'ALLOW_COMMENTS', False)


@register.assignment_tag
def get_homepage_events():
    """Returns 3 latest news posts"""
    today = date.today()
    events = Event.objects.live().filter(
        date_from__gte=today).order_by('date_from')
    if events.count() < 4:
        return events
    else:
        return events[:4]


@register.assignment_tag
def get_news_preview():
    """Returns 3 latest news posts"""
    today = date.today()
    pages = NewsPost.objects.live().filter(date__lte=today).order_by('-date')
    if pages.count() < 3:
        return pages
    else:
        return pages[:3]


@register.assignment_tag
def get_blog_posts_preview():
    """Returns 3 latest blog posts"""
    today = date.today()
    pages = BlogPost.objects.live().filter(date__lte=today).order_by('-date')
    if pages.count() < 4:
        return pages
    else:
        return pages[:4]


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.
    Object-comparison to self will return false as objects would differ.

    :rtype: `wagtail.wagtailcore.models.Page`
    """
    return context['request'].site.root_page


@register.assignment_tag(takes_context=False)
def get_twitter_name():
    return getattr(settings, 'TWITTER_NAME')


@register.assignment_tag(takes_context=False)
def get_twitter_url():
    return getattr(settings, 'TWITTER_URL')


@register.assignment_tag(takes_context=False)
def get_twitter_widget_id():
    return getattr(settings, 'TWITTER_WIDGET_ID')


@register.simple_tag
def has_view_restrictions(page):
    """Returns True if the page has view restrictions set up, False
    otherwise."""
    return page.view_restrictions.count() > 0


@register.inclusion_tag('cms/tags/main_menu.html', takes_context=True)
def main_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = (current_page.url == root.url
                   if current_page else False)

    for page in menu_pages:
        page.active = (current_page.url.startswith(page.url)
                       if current_page else False)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}


@register.inclusion_tag('cms/tags/sub_menu.html', takes_context=True)
def sub_menu(context, root):
    """Returns the sub menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    return {'request': context['request'], 'root': root,
            'menu_pages': menu_pages}


@register.inclusion_tag('cms/tags/footer_menu.html', takes_context=True)
def footer_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().live().in_menu()

    root.active = (current_page.url == root.url
                   if current_page else False)

    for page in menu_pages:
        page.active = (current_page.url.startswith(page.url)
                       if current_page else False)

    return {'request': context['request'], 'root': root,
            'current_page': current_page, 'menu_pages': menu_pages}

'''GN: 

{% toc %}
    <h1>first title</h1>
    <h1>second title</h1>
{% endtoc %}

toc tag adds a name="first-title" to the headings
and adds a new toc list to the context.
Each item in the list as the form: 
{
    'title': 'first title'
    'slug': 'first-title'
}

The toc variable can be used to build a
dynamic table of content.

Use class="not-in-toc" to exclude a heading from the toc.
'''


@register.tag(name="toc")
def do_table_of_contents(parser, token):
    nodelist = parser.parse(('endtoc',))
    parser.delete_first_token()
    return TableOfContentsNode(nodelist)


class TableOfContentsNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        from django.utils.text import slugify
        from django.utils.html import strip_tags

        output = self.nodelist.render(context)

        toc = []

        def replace_title(m):
            ret = m.group(0)

            title = m.group(4)
            title = strip_tags(title).strip()
            slug = slugify(title)

            if title and NOT_IN_TOC not in m.group(3):
                toc.append({
                    'title': title,
                    'slug': slug
                })

            if slug:
                ret = '%s%s id="%s"%s%s%s' % (
                    m.group(1),
                    m.group(2),
                    slug,
                    m.group(3),
                    m.group(4),
                    m.group(5),
                )

            return ret

        output = re.sub(r'(?s)(<h)(\d)([^>]*>)(.*?)(</h\2>)', replace_title, output)

        context['toc'] = toc

        return output
