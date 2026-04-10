import logging
import re

import httpx
from bs4 import BeautifulSoup

from fetcher.base import FetchedServer, PlayerCount, ServerFetcher

logger = logging.getLogger(__name__)

MAX_PAGES = 50


class BestMinecraftServersFetcher(ServerFetcher):
    source_name = "best-minecraft-servers"
    priority = 5
    base_url = "https://best-minecraft-servers.co"

    async def fetch_servers(self):
        async with httpx.AsyncClient(
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            follow_redirects=True,
            timeout=30,
        ) as client:
            for page in range(1, MAX_PAGES + 1):
                url = f"{self.base_url}/pg.{page}" if page > 1 else self.base_url
                try:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        break
                except httpx.HTTPError:
                    logger.exception(f"Failed to fetch page {page}")
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                rows = soup.select("table.servers tbody tr")
                if not rows:
                    break

                for row in rows:
                    server = self._parse_row(row)
                    if server:
                        yield server

    def _parse_row(self, row) -> FetchedServer | None:
        # Server link and ID
        name_link = row.select_one("td.name h3.server-name a")
        if not name_link:
            return None

        href = name_link.get("href", "")
        # href like "/server-complex-gaming.2763"
        match = re.search(r"\.(\d+)$", href)
        if not match:
            return None
        external_id = match.group(1)
        name = name_link.get_text(strip=True)

        # IP
        ip = ""
        copy_el = row.select_one("[data-clipboard-text]")
        if copy_el:
            ip = copy_el.get("data-clipboard-text", "")

        # Port
        port = 25565
        port_el = row.select_one("[data-port]")
        if port_el:
            try:
                port = int(port_el.get("data-port", "25565"))
            except ValueError:
                pass

        # Description
        desc_el = row.select_one("p.description")
        description = desc_el.get_text(strip=True) if desc_el else ""

        # Players
        online_players = 0
        max_players = 0
        players_td = row.select_one("td.players")
        if players_td:
            text = players_td.get_text(strip=True)
            m = re.match(r"(\d[\d,]*)/(\d[\d,]*)", text)
            if m:
                online_players = int(m.group(1).replace(",", ""))
                max_players = int(m.group(2).replace(",", ""))

        is_online = online_players > 0

        return FetchedServer(
            external_id=external_id,
            name=name,
            ip_address=ip,
            port=port,
            description=description,
            online_players=online_players,
            max_players=max_players,
            is_online=is_online,
            source_url=f"{self.base_url}{href}",
        )

    async def fetch_player_counts(self):
        async for server in self.fetch_servers():
            yield PlayerCount(
                external_id=server.external_id,
                online_players=server.online_players,
                is_online=server.is_online,
            )
