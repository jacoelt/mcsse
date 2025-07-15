import logging


from core.models import ServerTag
from fetcher.fetched_server import FetchedServer
from fetcher.helpers.countries import get_country_code
from fetcher.helpers.webpage_getter import WebpageGetter
from fetcher.server_fetcher_base import ServerFetcherBase
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class MinecraftServersFetcher(ServerFetcherBase):
    server_list_url = "https://minecraftservers.org/index/{page_number}"
    individual_server_url = "https://minecraftservers.org/server/{server_id}"
    banner_full_url = "https://minecraftservers.org{banner_url}"
    max_page_number = 898

    def __init__(self):
        pass

    async def get_all_servers(self) -> list[FetchedServer]:

        # Get server list webpage content
        webpage_getter = WebpageGetter()

        # Creating generator for all pages
        pages_content = webpage_getter.get(
            urls=[
                self.server_list_url.format(page_number=page_number)
                for page_number in range(1, self.max_page_number + 1)
            ],
            wait_for_class="server-list",
            delay_between_page_loads=0,
            max_concurrent_requests=10,
        )

        # Parse the content to extract server list
        logger.info("Fetching and parsing server list content...")
        server_ids = set()
        async for page_content in pages_content:
            soup = BeautifulSoup(page_content, "html.parser")
            server_links = soup.select("div.server div.banner a")

            for link in server_links:
                # Extract server ID from the link
                try:
                    url_parts = link["href"].split("/")
                    if url_parts[-1] != "":
                        server_id = url_parts[-1]
                    else:
                        server_id = url_parts[-2]
                    server_ids.add(server_id)
                except (IndexError, KeyError):
                    logger.warning("No valid href found in the server link, skipping.")

        logger.info(f"Found {len(server_ids)} unique server IDs.")

        # For each server in the list:
        # Get server details webpage content from the individual server URL
        # Parse the content to extract server details
        # Create a Server object

        server_pages = webpage_getter.get(
            urls=[
                self.individual_server_url.format(server_id=server_id)
                for server_id in server_ids
            ],
            wait_for_class="server-info",
            delay_between_page_loads=0,
            max_concurrent_requests=10,
        )

        logger.info("Parsing individual server content...")
        servers = []
        error_list = []
        async for server_page_content in server_pages:
            if not server_page_content:
                continue

            try:
                server = self._parse_server_content(server_page_content)
            except Exception as e:
                logger.critical(f"Error parsing server content: {e}")
                error_list.append(e)
                continue

            servers.append(server)

        if error_list:
            raise ExceptionGroup(
                "Errors occurred while parsing server content",
                error_list,
            )

        logger.info(f"Parsed {len(servers)} servers successfully.")
        return servers

    def _parse_server_content(self, server_page_content: str) -> list[FetchedServer]:
        soup = BeautifulSoup(server_page_content, "html.parser")

        server = FetchedServer()
        server.name = self._parse_text_from_selector(
            soup,
            "section div.row div.header-bar div.text",
        )

        server.description = self._parse_text_from_selector(
            soup,
            "section div.row #info p.desc",
        )

        server_data_block = soup.select_one("section div.row div.server-info")
        if not server_data_block:
            return server

        def get_text_from_server_data_block(
            label: str,
            element: str = None,
            attribute: str = None,
        ) -> str:
            try:
                block = server_data_block.select_one(
                    f"div.row div:first-child:-soup-contains('{label}')"
                ).parent.select("div")[1]
                if not block:
                    return None

                if element:
                    block = block.select_one(element)
                    if not block:
                        return None

                if attribute:
                    return block.get(attribute, "").strip()

                return block.get_text(strip=True)

            except (AttributeError, KeyError):
                return None

        server.ip_address_java = get_text_from_server_data_block(
            "Java IP",
            "span",
        ) or get_text_from_server_data_block(
            "IP",
            "span",
        )

        server.ip_address_bedrock = get_text_from_server_data_block(
            "Bedrock IP",
            "span",
        )

        try:
            server.banner = self.banner_full_url.format(
                banner_url=soup.select_one("section div.row #info img.banner")["src"]
            )
        except (AttributeError, KeyError):
            pass

        server.versions = [get_text_from_server_data_block("Version", "a")]

        players_str = get_text_from_server_data_block("Players")
        try:
            players_online, max_players = map(
                int, players_str.split("/") if "/" in players_str else (players_str, 0)
            )
            server.players_online = players_online
            server.max_players = max_players
        except (ValueError, TypeError):
            pass

        status_str = get_text_from_server_data_block("Status")
        if not status_str:
            server.status = "unknown"
        elif "online" in status_str:
            server.status = "online"
        elif "offline" in status_str:
            server.status = "offline"
        else:
            server.status = "unknown"

        server.total_votes = int(get_text_from_server_data_block("Votes") or 0)

        server.country = get_country_code(
            get_text_from_server_data_block("Country"),
            raise_not_found=False,
        )

        server.website = get_text_from_server_data_block("Website", "a", "href")

        server.discord = get_text_from_server_data_block("Discord", "a", "href")

        server.tags = self._parse_server_tags(soup)

        return server

    def _parse_text_from_selector(self, soup: BeautifulSoup, selector: str) -> str:
        element = soup.select_one(selector)
        if element:
            element_texts = element.find_all(string=True)
            if element_texts:
                return "\n".join([element.strip() for element in element_texts])

        return ""

    def _parse_server_tags(self, soup: BeautifulSoup) -> list[ServerTag]:
        tag_container = soup.select_one("div.row.tags div:nth-child(2)")
        if not tag_container:
            return []
        tags = []
        for tag in tag_container.select("a.button"):
            tag_name = tag.get_text(strip=True)
            if tag_name:
                tags.append(ServerTag(name=tag_name))

        return tags
