import logging
import re

import httpx
from bs4 import BeautifulSoup

from fetcher.base import FetchedServer, PlayerCount, ServerFetcher

logger = logging.getLogger(__name__)

MAX_PAGES = 50


class MinecraftBuzzFetcher(ServerFetcher):
    source_name = "minecraft-buzz"
    priority = 8
    base_url = "https://minecraft.buzz"

    async def fetch_servers(self):
        async with httpx.AsyncClient(
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            follow_redirects=True,
            timeout=30,
        ) as client:
            for page in range(1, MAX_PAGES + 1):
                url = f"{self.base_url}/page/{page}" if page > 1 else self.base_url
                try:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        break
                except httpx.HTTPError:
                    logger.exception(f"Failed to fetch page {page}")
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                rows = soup.select("tr.server-row.server-listing")
                if not rows:
                    break

                for row in rows:
                    server = self._parse_row(row)
                    if server:
                        yield server

    def _parse_row(self, row) -> FetchedServer | None:
        external_id = row.get("id", "")
        if not external_id:
            return None

        # Name
        name_el = row.select_one("h3")
        name = name_el.get_text(strip=True) if name_el else ""

        # IP
        ip = ""
        ip_el = row.select_one("data.ip-block")
        if ip_el:
            ip = ip_el.get("value", "") or ip_el.get_text(strip=True)

        # Banner
        banner_url = ""
        banner_img = row.select_one("img[src*='banner'], img[src*='favicons']")
        if banner_img:
            banner_url = banner_img.get("src", "")

        # Version and tags
        version = ""
        tags = []
        edition = "java"
        badges = row.select("span.badge")
        for badge in badges:
            text = badge.get_text(strip=True)
            icon = badge.select_one("i")
            if icon and "fa-wrench" in icon.get("class", []):
                # Version badge
                version = text.replace("Version", "").strip()
            elif icon and "fa-tag" in icon.get("class", []):
                # Tag/gamemode
                tag = text.replace("Server", "").strip()
                if tag:
                    tags.append(tag)
            elif icon and "fa-gamepad" in icon.get("class", []):
                # Edition
                if "Cross Platform" in text or "Bedrock" in text:
                    edition = "both"

        # Players
        online_players = 0
        max_players = 0
        # Look for the players cell
        for td in row.select("td"):
            text = td.get_text(strip=True)
            m = re.match(r"^(\d[\d,]*)/(\d[\d,]*)$", text)
            if m:
                online_players = int(m.group(1).replace(",", ""))
                max_players = int(m.group(2).replace(",", ""))
                break

        # Status
        is_online = False
        status_el = row.select_one("data[value='Online']")
        if status_el:
            is_online = True

        # Description
        description = ""
        desc_el = row.select_one("td.text-black-50.text-break p")
        if desc_el:
            description = desc_el.get_text(strip=True)

        return FetchedServer(
            external_id=external_id,
            name=name,
            ip_address=ip,
            game_version=version,
            edition=edition,
            online_players=online_players,
            max_players=max_players,
            is_online=is_online,
            tags=tags,
            banner_url=banner_url,
            description=description,
            source_url=f"{self.base_url}/server/{external_id}",
        )

    async def fetch_player_counts(self):
        async for server in self.fetch_servers():
            yield PlayerCount(
                external_id=server.external_id,
                online_players=server.online_players,
                is_online=server.is_online,
            )
