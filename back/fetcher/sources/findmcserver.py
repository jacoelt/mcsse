import logging

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)


class FindMCServerFetcher(ServerFetcher):
    """findmcserver.com — blocked by Cloudflare WAF."""

    source_name = "findmcserver"
    priority = 6
    base_url = "https://findmcserver.com"

    async def fetch_servers(self):
        logger.warning(
            f"{self.source_name}: skipped — site blocks automated requests (Cloudflare WAF). "
            "Needs browser automation (Playwright) to scrape."
        )
        return
        yield  # make this a generator
