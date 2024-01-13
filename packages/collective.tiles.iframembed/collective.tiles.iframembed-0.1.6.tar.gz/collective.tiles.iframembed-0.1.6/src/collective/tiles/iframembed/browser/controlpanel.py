# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from collective.tiles.iframembed.interfaces import IIFrameEmbedTilesSettings  # noqa
from collective.tiles.iframembed import _


class CollectiveTilesIframeEmbedEditForm(controlpanel.RegistryEditForm):
    """settings form."""
    schema = IIFrameEmbedTilesSettings
    id = "TilesIframeEmbedSettingsEditForm"
    label = _('tiles_iframembed_settings_label', u'IFrame Embed Tile Settings')
    description = u""


class CollectiveTilesIframeEmbedSettingsControlPanel(controlpanel.ControlPanelFormWrapper):  # noqa
    """Analytics settings control panel.
    """
    form = CollectiveTilesIframeEmbedEditForm
