# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.textfield import RichText
from collective.tiles.iframembed import _
from zope import schema
from plone.supermodel import model
from zope.interface import Interface


class ICollectiveTilesIframembedLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IFrameEmbedTile(model.Schema):
    title = schema.TextLine(
        title=_('label_tile_title', u'Tile title'),
        required=True
    )

    show_title = schema.Bool(
        title=_('label_show_tile', u'Show tile title'),
        required=False,
        default=False
    )

    url_to_embed = schema.TextLine(
        title=_('label_url_to_embed', u'Url to embed'),
        required=False
    )

    width = schema.TextLine(
        title=_('label_tile_width', u'width'),
        required=False
    )

    height = schema.TextLine(
        title=_('label_tile_heigth', u'height'),
        required=False
    )

    frameborder = schema.TextLine(
        title=_('label_tile_frameborder', u'frameborder'),
        required=False
    )

    allowfullscreen = schema.TextLine(
        title=_('label_tile_allowfullscreen', u'allowfullscreen'),
        required=False
    )

    style = schema.TextLine(
        title=_('label_tile_style', u'style'),
        required=False
    )

    scrolling = schema.TextLine(
        title=_('label_tile_scrolling', u'scrolling'),
        required=False
    )

    allowTransparency = schema.TextLine(
        title=_('label_tile_allowTransparency', u'allowTransparency'),
        required=False
    )


class IIFrameEmbedTilesSettings(Interface):
    """ """
    available_domains = schema.Tuple(
        title=_(u'Allowed domains'),
        description=_(u"One value for row"),
        missing_value=None,

        value_type=schema.TextLine()
    )
