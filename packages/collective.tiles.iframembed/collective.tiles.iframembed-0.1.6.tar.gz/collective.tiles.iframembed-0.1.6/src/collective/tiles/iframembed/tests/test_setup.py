# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.tiles.iframembed.testing import COLLECTIVE_TILES_IFRAMEMBED_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.tiles.iframembed is properly installed."""

    layer = COLLECTIVE_TILES_IFRAMEMBED_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.tiles.iframembed is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.tiles.iframembed'))

    def test_browserlayer(self):
        """Test that ICollectiveTilesIframembedLayer is registered."""
        from collective.tiles.iframembed.interfaces import (
            ICollectiveTilesIframembedLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveTilesIframembedLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_TILES_IFRAMEMBED_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.tiles.iframembed'])

    def test_product_uninstalled(self):
        """Test if collective.tiles.iframembed is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.tiles.iframembed'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveTilesIframembedLayer is removed."""
        from collective.tiles.iframembed.interfaces import ICollectiveTilesIframembedLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveTilesIframembedLayer, utils.registered_layers())
