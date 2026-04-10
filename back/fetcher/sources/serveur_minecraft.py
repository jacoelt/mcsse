import logging

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)


class ServeurMinecraftFetcher(ServerFetcher):
    """serveur-minecraft.com — requires Cloudflare JS challenge bypass."""

    source_name = "serveur-minecraft"
    priority = 9
    base_url = "https://serveur-minecraft.com"

    async def fetch_servers(self):
        logger.warning(
            f"{self.source_name}: skipped — site is behind Cloudflare JS challenge. "
            "Needs browser automation (Playwright) to scrape."
        )
        return
        yield  # make this a generator
