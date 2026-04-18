import logging
import re

import httpx
from bs4 import BeautifulSoup

from fetcher.base import FetchedServer, PlayerCount, ServerFetcher

logger = logging.getLogger(__name__)


class MinecraftServersOrgFetcher(ServerFetcher):
    source_name = "minecraftservers-org"
    priority = 2
    base_url = "https://minecraftservers.org"

    async def fetch_servers(self):
        # Disable redirect following: past-the-end pages 3xx-redirect away
        # (sometimes in loops), which we treat as end-of-list.
        async with httpx.AsyncClient(
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            follow_redirects=False,
            timeout=30,
        ) as client:
            page = 1
            while True:
                url = f"{self.base_url}/index/{page}" if page > 1 else self.base_url
                try:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        break
                except httpx.HTTPError:
                    logger.exception(f"Failed to fetch page {page}")
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                listings = soup.select("div.server-listing")
                if not listings:
                    break

                logger.debug("%s: page %d, %d listings", self.source_name, page, len(listings))

                for listing in listings:
                    server = self._parse_listing(listing)
                    if server:
                        yield server

                page += 1

    def _parse_listing(self, listing) -> FetchedServer | None:
        external_id = listing.get("data-id", "")
        if not external_id:
            return None

        # Name
        name_el = listing.select_one(".name a")
        name = name_el.get_text(strip=True) if name_el else ""

        # IP address from copy button
        ip = ""
        copy_el = listing.select_one("[data-clipboard-content]")
        if copy_el:
            ip = copy_el.get("data-clipboard-content", "")

        # Players
        online_players = 0
        max_players = 0
        players_el = listing.select_one(".players .value")
        if players_el:
            text = players_el.get_text(strip=True)
            m = re.match(r"(\d[\d,]*)/(\d[\d,]*)", text)
            if m:
                online_players = int(m.group(1).replace(",", ""))
                max_players = int(m.group(2).replace(",", ""))

        # Status
        is_online = False
        status_el = listing.select_one(".status .value")
        if status_el and "online" in status_el.get_text(strip=True).lower():
            is_online = True

        # Banner
        banner_url = ""
        banner_img = listing.select_one(".banner img")
        if banner_img:
            src = banner_img.get("src", "")
            if src:
                banner_url = f"{self.base_url}{src}" if src.startswith("/") else src

        return FetchedServer(
            external_id=external_id,
            name=name,
            ip_address=ip,
            online_players=online_players,
            max_players=max_players,
            is_online=is_online,
            banner_url=banner_url,
            source_url=f"{self.base_url}/server/{external_id}",
        )

    async def fetch_player_counts(self):
        async for server in self.fetch_servers():
            yield PlayerCount(
                external_id=server.external_id,
                online_players=server.online_players,
                is_online=server.is_online,
            )
