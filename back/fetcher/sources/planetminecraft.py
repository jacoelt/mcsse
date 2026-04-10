import logging

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)


class PlanetMinecraftFetcher(ServerFetcher):
    """planetminecraft.com — JS-rendered, requires browser automation."""

    source_name = "planetminecraft"
    priority = 4
    base_url = "https://www.planetminecraft.com"

    async def fetch_servers(self):
        logger.warning(
            f"{self.source_name}: skipped — site is JS-rendered. "
            "Needs browser automation (Playwright) to scrape."
        )
        return
        yield  # make this a generator
