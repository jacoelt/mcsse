import logging
import re

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)

MAX_PAGES = 50


class ServeurMinecraftFetcher(ServerFetcher):
    """serveur-minecraft.com — Cloudflare-protected, scraped via curl_cffi browser TLS impersonation."""

    source_name = "serveur-minecraft"
    priority = 9
    base_url = "https://serveur-minecraft.com"

    async def fetch_servers(self):
        seen: set[str] = set()
        async with AsyncSession(impersonate="chrome", timeout=30) as client:
            for page in range(1, MAX_PAGES + 1):
                url = f"{self.base_url}/?page={page}" if page > 1 else f"{self.base_url}/"
                try:
                    resp = await client.get(url)
                except Exception:
                    logger.exception(f"{self.source_name}: failed page {page}")
                    break
                if resp.status_code != 200:
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                entries = soup.select(".row.entry")
                if not entries:
                    break

                new_on_page = 0
                for entry in entries:
                    server = self._parse_entry(entry)
                    if not server or server.external_id in seen:
                        continue
                    seen.add(server.external_id)
                    new_on_page += 1
                    yield server

                if new_on_page == 0:
                    break

    def _parse_entry(self, entry) -> FetchedServer | None:
        title_link = entry.select_one("h3.title a[href]")
        if not title_link:
            return None
        href = title_link.get("href", "")
        m = re.match(r"^/(\d+)$", href)
        if not m:
            return None
        external_id = m.group(1)
        name = title_link.get_text(strip=True)

        desc_el = entry.select_one(".desc")
        description = desc_el.get_text(" ", strip=True) if desc_el else ""

        tags = [t.get_text(strip=True) for t in entry.select(".tags a.badge") if t.get_text(strip=True)]

        online_players = 0
        max_players = 0
        players_el = entry.select_one(".player-info")
        if players_el:
            pm = re.search(r"(\d[\d\s]*)\s*/\s*(\d[\d\s]*)", players_el.get_text())
            if pm:
                try:
                    online_players = int(pm.group(1).replace(" ", "").replace("\xa0", ""))
                    max_players = int(pm.group(2).replace(" ", "").replace("\xa0", ""))
                except ValueError:
                    pass

        ip = ""
        addr_el = entry.select_one(".server-address")
        if addr_el:
            ip = addr_el.get("data-address", "") or addr_el.get_text(strip=True)

        votes = 0
        vote_el = entry.select_one(".vote-count")
        if vote_el:
            vm = re.search(r"(\d[\d\s]*)", vote_el.get_text())
            if vm:
                try:
                    votes = int(vm.group(1).replace(" ", "").replace("\xa0", ""))
                except ValueError:
                    pass

        banner_url = ""
        img = entry.select_one(".image img")
        if img:
            banner_url = img.get("src", "") or ""

        is_online = online_players > 0 or max_players > 0

        return FetchedServer(
            external_id=external_id,
            name=name,
            ip_address=ip,
            description=description,
            online_players=online_players,
            max_players=max_players,
            votes=votes,
            tags=tags,
            banner_url=banner_url,
            is_online=is_online,
            source_url=f"{self.base_url}{href}",
        )
