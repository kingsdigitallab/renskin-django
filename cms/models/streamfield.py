

from django import forms
from wagtail.core.blocks import (
    CharBlock, FieldBlock, PageChooserBlock, RawHTMLBlock, RichTextBlock,
    StreamBlock, StructBlock, TextBlock, URLBlock
)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock


class HTMLAlignmentChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('default', 'Default'), ('full', 'Full width'),
    ))


class AlignedHTMLBlock(StructBlock):
    html = RawHTMLBlock()
    alignment = HTMLAlignmentChoiceBlock()


class HomePageBlock(StructBlock):
    url = URLBlock(required=False)
    page = PageChooserBlock(required=False)
    title = CharBlock()
    description = RichTextBlock()

    class Meta:
        template = 'cms/blocks/home_page_block.html'
        help_text = '''
        Use either URL or page, if both are filled in URL takes precedence.
        For an email button, use the format mailto:email@address.com'''


class ImageFormatChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'), ('right', 'Wrap right'),
        ('mid', 'Mid width'), ('full-width', 'Full width'),
        ('hero', 'Hero'),
    ))


class ImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = RichTextBlock()
    alignment = ImageFormatChoiceBlock()

    class Meta:
        template = 'cms/blocks/image_block.html'


class LinkStyleChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('default', 'Default'), ('button', 'Button'),
    ))


class LinkBlock(StructBlock):
    url = CharBlock(required=False)
    page = PageChooserBlock(required=False)
    label = CharBlock()
    style = LinkStyleChoiceBlock()

    class Meta:
        help_text = '''
        Use either URL or page, if both are filled in URL takes precedence.'''
        template = 'cms/blocks/link_block.html'


class PullQuoteStyleChoiceBlock(FieldBlock):
    field = forms.ChoiceField(choices=(
        ('default', 'Default'), ('with-background', 'With background image'),
    ))


class PullQuoteBlock(StructBlock):
    quote = TextBlock('quote title')
    attribution = CharBlock()
    affiliation = CharBlock(required=False)
    style = PullQuoteStyleChoiceBlock()

    class Meta:
        template = 'cms/blocks/pull_quote_block.html'


class CMSStreamBlock(StreamBlock):
    # home = HomePageBlock(icon='grip', label='Homepage Block')

    h2 = CharBlock(icon='title', classname='title')
    h3 = CharBlock(icon='title', classname='title')
    h4 = CharBlock(icon='title', classname='title')
    h5 = CharBlock(icon='title', classname='title')

    intro = RichTextBlock(icon='pilcrow')
    paragraph = RichTextBlock(icon='pilcrow')
    pullquote = PullQuoteBlock(icon='openquote')

    image = ImageBlock(label='Aligned image', icon='image')
    document = DocumentChooserBlock(icon='doc-full-inverse')
    link = LinkBlock(icon='link')
    embed = EmbedBlock(icon='media', max_length=2048)

    html = AlignedHTMLBlock(icon='code', label='Raw HTML')
