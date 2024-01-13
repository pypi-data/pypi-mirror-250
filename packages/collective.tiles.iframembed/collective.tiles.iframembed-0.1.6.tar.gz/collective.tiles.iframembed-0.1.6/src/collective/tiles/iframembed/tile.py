# -*- encoding:utf-8 *-
from plone import tiles
from plone import api
from plone.app.uuid.utils import uuidToObject
from collective.tiles.iframembed.interfaces import IIFrameEmbedTilesSettings
from urlparse import urlparse


class FrameEmbedTile(tiles.PersistentTile):
    def iframe_validation(self):
        url_to_embed = self.data.get("url_to_embed")
        if not url_to_embed:
            return False

        valid_domains = api.portal.get_registry_record(
            "available_domains", interface=IIFrameEmbedTilesSettings
        )

        for domain in valid_domains:
            if url_to_embed.find(domain) != -1:
                return True

        api.portal.show_message(
            "L'url indicato non e' valido per i domini ammessi", self.request, "error"
        )
        return False

    def eval_query_string(self):
        o = urlparse(self.request.HTTP_REFERER)
        query_string = o.query
        if (
            query_string.startswith("_authenticator")
            or "SearchableText" in query_string
        ):
            return (self.data.get("url_to_embed")).rstrip("/")

        query_string = query_string.replace("?", "/", 1)
        query_string = query_string.replace("&", "?", 1)
        result = "%s/%s" % (self.data.get("url_to_embed"), query_string)
        return result.rstrip("/")
