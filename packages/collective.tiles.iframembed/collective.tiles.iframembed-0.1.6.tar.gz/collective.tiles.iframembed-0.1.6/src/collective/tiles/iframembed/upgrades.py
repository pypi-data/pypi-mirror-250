from collective.tiles.iframembed.setuphandlers import post_install
from plone import api


def add_default_domains(context):
    """ """
    context.runAllImportStepsFromProfile('profile-collective.tiles.iframembed:cleanup')

    USED_DOMAINS = api.portal.get_registry_record(
        'collective.tiles.iframembed.interfaces.IIFrameEmbedTilesSettings.available_domains',
        default=()
    )
    context.runImportStepFromProfile('profile-collective.tiles.iframembed:default', 'plone.app.registry')
    
    DOMAINS = (
        u'https://www.facebook.com',
        u'https://www.youtube.com',
        u'https://www.regione.emilia-romagna.it',
        u'https://www2.regione.emilia-romagna.it',
    )

    FILTERED = [x for x in DOMAINS if x not in USED_DOMAINS]
    
    if not FILTERED:
        return

    USED_DOMAINS = USED_DOMAINS + tuple(FILTERED)

    api.portal.set_registry_record(
        'collective.tiles.iframembed.interfaces.IIFrameEmbedTilesSettings.available_domains',
        USED_DOMAINS
    )