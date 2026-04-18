import logging
import re

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)


class PlanetMinecraftFetcher(ServerFetcher):
    """planetminecraft.com — JS-rendered listing, scraped via curl_cffi browser TLS impersonation."""

    source_name = "planetminecraft"
    priority = 4
    base_url = "https://www.planetminecraft.com"

    async def fetch_servers(self):
        # Disable redirect following: past-the-end pages 3xx-redirect away
        # (sometimes in loops), which we treat as end-of-list.
        seen: set[str] = set()
        async with AsyncSession(impersonate="chrome", timeout=30) as client:
            page = 1
            while True:
                url = (
                    f"{self.base_url}/servers/?p={page}"
                    if page > 1
                    else f"{self.base_url}/servers/"
                )
                try:
                    resp = await client.get(url, allow_redirects=False)
                except Exception:
                    logger.exception(f"{self.source_name}: failed page {page}")
                    break
                if resp.status_code != 200:
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                items = soup.select("li.resource_server_item")
                if not items:
                    break

                logger.debug("%s: page %d, %d items", self.source_name, page, len(items))

                new_on_page = 0
                for item in items:
                    server = self._parse_item(item)
                    if not server or server.external_id in seen:
                        continue
                    seen.add(server.external_id)
                    new_on_page += 1
                    yield server

                if new_on_page == 0:
                    break

                page += 1

    def _parse_item(self, item) -> FetchedServer | None:
        title = item.select_one("a.server-title")
        if not title:
            return None
        href = title.get("href", "")
        # /server/<slug>/ — use slug (incl. numeric suffix when present) as stable ID
        m = re.match(r"^/server/([^/]+)/?", href)
        if not m:
            return None
        external_id = m.group(1)

        name = ""
        name_el = title.select_one(".txt")
        if name_el:
            name = name_el.get_text(strip=True)
        else:
            name = (title.get("title") or "").strip()

        banner_url = ""
        img = title.select_one("img")
        if img:
            banner_url = img.get("src", "") or ""

        # Votes: first numeric span in .r-stats (associated with the star icon)
        votes = 0
        stats = item.select_one(".r-stats")
        if stats:
            first_span = stats.select_one("span")
            if first_span:
                try:
                    votes = int(first_span.get_text(strip=True).replace(",", ""))
                except ValueError:
                    pass

        # Online status + players: "3/40 players"
        online_players = 0
        max_players = 0
        is_online = False
        status_el = item.select_one(".online_status")
        if status_el:
            text = status_el.get_text(" ", strip=True)
            if "Online" in text:
                is_online = True
            pm = re.search(r"(\d[\d,]*)/(\d[\d,]*)", text)
            if pm:
                try:
                    online_players = int(pm.group(1).replace(",", ""))
                    max_players = int(pm.group(2).replace(",", ""))
                except ValueError:
                    pass

        # Country from flag class
        country = ""
        flag = item.select_one(".flag")
        if flag:
            for c in flag.get("class", []):
                cm = re.match(r"^flag-([a-z]{2})$", c)
                if cm:
                    country = cm.group(1).upper()
                    break

        source_url = href
        if source_url.startswith("/"):
            source_url = f"{self.base_url}{source_url}"

        return FetchedServer(
            external_id=external_id,
            name=name,
            votes=votes,
            country=country,
            banner_url=banner_url,
            online_players=online_players,
            max_players=max_players,
            is_online=is_online,
            source_url=source_url,
        )
