import logging
import re

import httpx
from bs4 import BeautifulSoup

from fetcher.base import FetchedServer, PlayerCount, ServerFetcher

logger = logging.getLogger(__name__)

MAX_PAGES = 50


class MinecraftMPFetcher(ServerFetcher):
    source_name = "minecraft-mp"
    priority = 1
    base_url = "https://minecraft-mp.com"

    async def fetch_servers(self):
        async with httpx.AsyncClient(
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            follow_redirects=True,
            timeout=30,
        ) as client:
            for page in range(1, MAX_PAGES + 1):
                url = f"{self.base_url}/servers/list/{page}/" if page > 1 else self.base_url
                try:
                    resp = await client.get(url)
                    if resp.status_code != 200:
                        break
                except httpx.HTTPError:
                    logger.exception(f"Failed to fetch page {page}")
                    break

                soup = BeautifulSoup(resp.text, "lxml")
                rows = soup.select("table.servers-table tbody tr")
                if not rows:
                    break

                for row in rows:
                    server = self._parse_row(row)
                    if server:
                        yield server

    def _parse_row(self, row) -> FetchedServer | None:
        # Server link and ID
        link = row.select_one("a[href^='/server-s']")
        if not link:
            return None

        href = link.get("href", "")
        match = re.search(r"/server-s(\d+)", href)
        if not match:
            return None
        external_id = match.group(1)

        # Name
        name_el = row.select_one("h3 a, .server-title-responsive a")
        name = name_el.get_text(strip=True) if name_el else ""

        # IP address
        ip = ""
        ip_el = row.select_one(".btn-server-ip")
        if ip_el:
            ip = ip_el.get_text(strip=True)
        else:
            copy_btn = row.select_one("[data-clipboard-text]")
            if copy_btn:
                ip = copy_btn.get("data-clipboard-text", "")

        # Country
        country = ""
        flag_img = row.select_one("img[src*='flags']")
        if flag_img:
            country_name = flag_img.get("alt", "")
            country = _country_name_to_code(country_name)

        # Description
        desc_el = row.select_one(".server-description, .server-description-responsive")
        description = desc_el.get_text(strip=True) if desc_el else ""

        # Players
        online_players = 0
        max_players = 0
        is_online = False
        player_el = row.select_one("button.btn-xs-playercount strong, .col-md-12 .players .value, td:last-child .players .value")
        if player_el:
            # Try the button format first: "471 / 500"
            player_btn = row.select_one("button.btn-xs-playercount")
            if player_btn:
                text = player_btn.get_text(strip=True)
                m = re.search(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)", text)
                if m:
                    online_players = int(m.group(1).replace(",", ""))
                    max_players = int(m.group(2).replace(",", ""))
        else:
            # Try the desktop format
            for btn in row.select("button.btn-default"):
                text = btn.get_text(strip=True)
                m = re.search(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)", text)
                if m:
                    online_players = int(m.group(1).replace(",", ""))
                    max_players = int(m.group(2).replace(",", ""))
                    break

        # Status
        status_btn = row.select_one("button.btn-success")
        if status_btn and "Online" in status_btn.get_text():
            is_online = True

        # Tags
        tags = []
        for tag_el in row.select(".list-server-tags a.btn-tag"):
            tags.append(tag_el.get_text(strip=True))

        # Version
        version = ""
        version_el = row.select_one("a.btn-version-fade")
        if version_el:
            version = version_el.get_text(strip=True)

        # Banner
        banner_url = ""
        banner_img = row.select_one(".server-card img[src*='banner']")
        if banner_img:
            banner_url = banner_img.get("src", "")
            if banner_url and not banner_url.startswith("http"):
                banner_url = f"{self.base_url}{banner_url}"

        return FetchedServer(
            external_id=external_id,
            name=name,
            ip_address=ip,
            description=description,
            game_version=version,
            online_players=online_players,
            max_players=max_players,
            is_online=is_online,
            country=country,
            tags=tags,
            banner_url=banner_url,
            source_url=f"{self.base_url}/server-s{external_id}",
        )

    async def fetch_player_counts(self):
        async for server in self.fetch_servers():
            yield PlayerCount(
                external_id=server.external_id,
                online_players=server.online_players,
                is_online=server.is_online,
            )


def _country_name_to_code(name: str) -> str:
    """Convert common country names to ISO 3166-1 alpha-2 codes."""
    mapping = {
        "united states of america": "US", "united states": "US", "usa": "US",
        "united kingdom": "GB", "great britain": "GB",
        "canada": "CA", "germany": "DE", "france": "FR",
        "australia": "AU", "brazil": "BR", "japan": "JP",
        "netherlands": "NL", "sweden": "SE", "finland": "FI",
        "russia": "RU", "poland": "PL", "spain": "ES",
        "italy": "IT", "mexico": "MX", "india": "IN",
        "china": "CN", "south korea": "KR", "singapore": "SG",
        "indonesia": "ID", "philippines": "PH", "turkey": "TR",
        "argentina": "AR", "chile": "CL", "colombia": "CO",
        "south africa": "ZA", "new zealand": "NZ", "ireland": "IE",
        "norway": "NO", "denmark": "DK", "belgium": "BE",
        "switzerland": "CH", "austria": "AT", "portugal": "PT",
        "czech republic": "CZ", "romania": "RO", "hungary": "HU",
        "ukraine": "UA", "thailand": "TH", "vietnam": "VN",
        "malaysia": "MY", "hong kong": "HK", "taiwan": "TW",
        "israel": "IL", "egypt": "EG", "pakistan": "PK",
        "bangladesh": "BD", "peru": "PE", "venezuela": "VE",
        "greece": "GR", "croatia": "HR", "serbia": "RS",
        "bulgaria": "BG", "slovakia": "SK", "lithuania": "LT",
        "latvia": "LV", "estonia": "EE", "slovenia": "SI",
    }
    return mapping.get(name.lower().strip(), "")
