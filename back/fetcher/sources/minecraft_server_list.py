import logging

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)


class MinecraftServerListFetcher(ServerFetcher):
    """minecraft-server-list.com — requires Cloudflare JS challenge bypass."""

    source_name = "minecraft-server-list"
    priority = 3
    base_url = "https://minecraft-server-list.com"

    async def fetch_servers(self):
        logger.warning(
            f"{self.source_name}: skipped — site is behind Cloudflare JS challenge. "
            "Needs browser automation (Playwright) to scrape."
        )
        return
        yield  # make this a generator
