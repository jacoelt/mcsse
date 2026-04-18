import logging

from curl_cffi.requests import AsyncSession

from fetcher.base import FetchedServer, ServerFetcher

logger = logging.getLogger(__name__)


class FindMCServerFetcher(ServerFetcher):
    """findmcserver.com — scraped via JSON API, Cloudflare-protected site requires browser TLS impersonation."""

    source_name = "findmcserver"
    priority = 6
    base_url = "https://findmcserver.com"

    async def fetch_servers(self):
        page_size = 500
        async with AsyncSession(impersonate="chrome", timeout=30) as client:
            page = 0
            while True:
                try:
                    resp = await client.get(
                        f"{self.base_url}/api/servers",
                        params={"pageNumber": page, "pageSize": page_size},
                    )
                except Exception:
                    logger.exception(f"{self.source_name}: request failed")
                    return

                if resp.status_code != 200:
                    logger.warning(f"{self.source_name}: status {resp.status_code}")
                    return

                try:
                    payload = resp.json()
                except Exception:
                    logger.exception(f"{self.source_name}: invalid JSON")
                    return

                items = payload.get("data", []) or []
                if not items:
                    return

                logger.debug("%s: page %d, %d items", self.source_name, page, len(items))

                for item in items:
                    server = self._parse_item(item)
                    if server:
                        yield server

                if len(items) < page_size:
                    return

                page += 1

    def _parse_item(self, item: dict) -> FetchedServer | None:
        external_id = item.get("id") or ""
        slug = item.get("slug") or ""
        if not external_id or not slug:
            return None

        # Address: prefer java, fall back to bedrock. Both can be "IP Address Hidden".
        java_addr = (item.get("javaAddress") or "").strip()
        bedrock_addr = (item.get("bedrockAddress") or "").strip()
        hidden_marker = "IP Address Hidden"
        ip = ""
        port = 25565
        edition = "java"
        if java_addr and java_addr != hidden_marker:
            ip = java_addr
            port = item.get("javaPort") or 25565
            edition = "java"
        elif bedrock_addr and bedrock_addr != hidden_marker:
            ip = bedrock_addr
            port = item.get("bedrockPort") or 19132
            edition = "bedrock"

        tags = []
        for tag in item.get("serverTags") or []:
            name = (tag.get("name") or "").strip()
            if name:
                tags.append(name)

        country = ""
        for loc in item.get("serverLocation") or []:
            name = (loc.get("name") or "").strip()
            if name:
                country = name
                break

        banner = ""
        bg = item.get("backgroundImage") or {}
        if isinstance(bg, dict):
            banner = bg.get("url") or ""
        if not banner:
            icon = item.get("iconImage") or {}
            if isinstance(icon, dict):
                banner = icon.get("url") or ""

        return FetchedServer(
            external_id=external_id,
            name=(item.get("name") or "").strip(),
            ip_address=ip,
            port=port,
            description=(item.get("shortDescription") or "").strip(),
            edition=edition,
            online_players=int(item.get("currentOnlinePlayers") or 0),
            max_players=int(item.get("currentMaxPlayers") or 0),
            votes=int(item.get("votes") or 0),
            country=country,
            tags=tags,
            banner_url=banner,
            is_online=bool(item.get("isOnline")),
            source_url=f"{self.base_url}/server/{slug}",
        )
