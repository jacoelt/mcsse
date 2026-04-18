import logging
import re

from bs4 import BeautifulSoup
from curl_cffi.requests import AsyncSession

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)


class MinecraftServerListFetcher(ServerFetcher):
    """minecraft-server-list.com — Cloudflare-protected, scraped via curl_cffi browser TLS impersonation."""

    source_name = "minecraft-server-list"
    priority = 3
    base_url = "https://minecraft-server-list.com"

    async def fetch_servers(self):
        # Disable redirect following: past-the-end pages 3xx-redirect away
        # (sometimes in loops), which we treat as end-of-list.
        seen: set[str] = set()
        async with AsyncSession(impersonate="chrome", timeout=30) as client:
            page = 1
            while True:
                url = (
                    f"{self.base_url}/page/{page}/" if page > 1 else f"{self.base_url}/"
                )
                try:
                    resp = await client.get(url, allow_redirects=False)
                except Exception:
                    logger.exception(f"{self.source_name}: failed page {page}")
                    break
                if resp.status_code != 200:
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                rows = soup.select("table tr")
                logger.debug("%s: page %d, %d rows", self.source_name, page, len(rows))
                parsed = 0
                for row in rows:
                    server = self._parse_row(row)
                    if not server or server.external_id in seen:
                        continue
                    seen.add(server.external_id)
                    parsed += 1
                    yield server
                if parsed == 0:
                    break

                page += 1

    def _parse_row(self, row) -> FetchedServer | None:
        # Server detail link: /server/411920/
        link = row.select_one("a[href*='/server/']")
        if not link:
            return None
        href = link.get("href", "")
        m = re.search(r"/server/(\d+)", href)
        if not m:
            return None
        external_id = m.group(1)

        name_el = row.select_one("h2.column-heading a") or link
        name = name_el.get_text(strip=True) if name_el else ""

        # IP is in the copy-ip input
        ip = ""
        ip_input = row.select_one("input.copylinkinput")
        if ip_input:
            ip = (ip_input.get("value") or "").strip()

        # Country flag class like "flag-us"
        country = ""
        flag = row.select_one("img.flag")
        if flag:
            for c in flag.get("class", []):
                cm = re.match(r"^flag-([a-z]{2})$", c)
                if cm:
                    country = cm.group(1).upper()
                    break

        # Banner image
        banner_url = ""
        banner = row.select_one("td.n2 img")
        if banner:
            src = banner.get("src", "")
            if src.startswith("//"):
                src = "https:" + src
            banner_url = src

        description = ""
        desc_el = row.select_one("div.serverListing")
        if desc_el:
            description = desc_el.get_text(" ", strip=True).rstrip(".")

        online_players = 0
        max_players = 0
        votes = 0
        n3 = row.select_one("td.n3")
        if n3:
            text = n3.get_text(" ", strip=True)
            pm = re.search(r"Players Online:\s*(\d[\d,]*)\s*/\s*(\d[\d,]*)", text)
            if pm:
                try:
                    online_players = int(pm.group(1).replace(",", ""))
                    max_players = int(pm.group(2).replace(",", ""))
                except ValueError:
                    pass
            vm = re.search(r"Votes \(all time\):\s*(\d[\d,]*)", text)
            if vm:
                try:
                    votes = int(vm.group(1).replace(",", ""))
                except ValueError:
                    pass
            if votes == 0:
                vm2 = re.search(r"Votes[^:]*:\s*(\d[\d,]*)", text)
                if vm2:
                    try:
                        votes = int(vm2.group(1).replace(",", ""))
                    except ValueError:
                        pass

        is_online = online_players > 0 or max_players > 0

        source_url = href
        if source_url.startswith("//"):
            source_url = "https:" + source_url
        elif source_url.startswith("/"):
            source_url = f"{self.base_url}{source_url}"

        return FetchedServer(
            external_id=external_id,
            name=name,
            ip_address=ip,
            description=description,
            online_players=online_players,
            max_players=max_players,
            votes=votes,
            country=country,
            banner_url=banner_url,
            is_online=is_online,
            source_url=source_url,
        )
