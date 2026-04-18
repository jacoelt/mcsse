import logging
import re

import httpx
from bs4 import BeautifulSoup

from fetcher.base import FetchedServer, PlayerCount, ServerFetcher

logger = logging.getLogger(__name__)


class TopGFetcher(ServerFetcher):
    source_name = "topg"
    priority = 7
    base_url = "https://topg.org"

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
                url = (
                    f"{self.base_url}/minecraft-servers/page/{page}"
                    if page > 1
                    else f"{self.base_url}/minecraft-servers/"
                )
                try:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        break
                except httpx.HTTPError:
                    logger.exception(f"Failed to fetch page {page}")
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                # Skip ad servers, only get real listings
                listings = soup.select(
                    "section#topg-server-list ul.topg-server-list li.topg-server"
                )
                if not listings:
                    break

                logger.debug("%s: page %d, %d listings", self.source_name, page, len(listings))

                for listing in listings:
                    if "ad-server" in listing.get("class", []):
                        continue
                    server = self._parse_listing(listing)
                    if server:
                        yield server

                page += 1

    def _parse_listing(self, listing) -> FetchedServer | None:
        # Server link and ID
        link = listing.select_one("a[href*='server-']")
        if not link:
            return None
        href = link.get("href", "")
        match = re.search(r"server-(\d+)", href)
        if not match:
            return None
        external_id = match.group(1)

        # Name
        name_el = listing.select_one("h3.topg-server-name")
        name = name_el.get_text(strip=True) if name_el else ""

        # IP
        ip = ""
        ip_el = listing.select_one("span.copy-ip[data-text]")
        if ip_el:
            ip = ip_el.get("data-text", "")

        # Players
        online_players = 0
        max_players = 0
        players_el = listing.select_one("span.topg-players")
        if players_el:
            spans = players_el.select("span")
            if len(spans) >= 2:
                try:
                    online_players = int(spans[0].get_text(strip=True).replace(",", ""))
                except ValueError:
                    pass
                max_text = spans[1].get_text(strip=True)
                if max_text != "∞":
                    try:
                        max_players = int(max_text.replace(",", ""))
                    except ValueError:
                        pass

        # Status
        is_online = False
        status_el = listing.select_one("span.topg-status")
        if status_el and "Online" in status_el.get_text():
            is_online = True

        # Tags and version
        tags = []
        version = ""
        for label in listing.select(".topg-col-about span.label"):
            text = label.get_text(strip=True)
            if re.match(r"^\d+\.\d+", text) or text == "Latest":
                if not version:
                    version = text
            elif text not in ("any",):
                tags.append(text)

        return FetchedServer(
            external_id=external_id,
            name=name,
            ip_address=ip,
            game_version=version,
            online_players=online_players,
            max_players=max_players,
            is_online=is_online,
            tags=tags,
            source_url=f"{self.base_url}/minecraft-servers/server-{external_id}",
        )

    async def fetch_player_counts(self):
        async for server in self.fetch_servers():
            yield PlayerCount(
                external_id=server.external_id,
                online_players=server.online_players,
                is_online=server.is_online,
            )
