# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.tiles.iframembed


class CollectiveTilesIframembedLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.tiles.iframembed)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.tiles.iframembed:default')


COLLECTIVE_TILES_IFRAMEMBED_FIXTURE = CollectiveTilesIframembedLayer()


COLLECTIVE_TILES_IFRAMEMBED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TILES_IFRAMEMBED_FIXTURE,),
    name='CollectiveTilesIframembedLayer:IntegrationTesting'
)


COLLECTIVE_TILES_IFRAMEMBED_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TILES_IFRAMEMBED_FIXTURE,),
    name='CollectiveTilesIframembedLayer:FunctionalTesting'
)


COLLECTIVE_TILES_IFRAMEMBED_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_TILES_IFRAMEMBED_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveTilesIframembedLayer:AcceptanceTesting'
)
