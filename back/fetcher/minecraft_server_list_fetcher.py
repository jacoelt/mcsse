from fetcher.helpers.countries import get_country_code
from fetcher.fetched_server import FetchedServer
from fetcher.helpers.webpage_getter import WebpageGetter
from fetcher.server_fetcher_base import ServerFetcherBase
from core.models import ServerTag
from bs4 import BeautifulSoup


class MinecraftServerListFetcher(ServerFetcherBase):
    server_list_url = "https://minecraft-server-list.com/page/{page_number}/"
    individual_server_url = "https://minecraft-server-list.com/server/{server_id}/"
    max_page_number = 300

    def __init__(self):
        pass

    async def get_all_servers(self) -> list[FetchedServer]:

        # Get server list webpage content
        webpage_getter = WebpageGetter()
        print("Fetching pages content...")
        pages_content = await webpage_getter.get(
            urls=[
                self.server_list_url.format(page_number=page_number)
                for page_number in range(1, self.max_page_number + 1)
            ],
            wait_for_class="serverdatadiv1",
            delay_between_page_loads=0,
            max_concurrent_requests=10,
            cache_only=True,
        )

        # Parse the content to extract server list
        print("Parsing server list content...")
        server_ids = set()
        for page_content in pages_content:
            soup = BeautifulSoup(page_content, "html.parser")
            server_links = soup.select("div.serverdatadiv1 table tbody td.n1 a")

            for link in server_links:
                # Extract server ID from the link
                href = link.get("href", "")
                if href:
                    server_id = href.split("/")[-2]
                    server_ids.add(server_id)
                else:
                    print("No href found in the server link, skipping.")

        print(f"Found {len(server_ids)} unique server IDs.")

        # For each server in the list:
        # Get server details webpage content from the individual server URL
        # Parse the content to extract server details
        # Create a Server object

        server_pages = await webpage_getter.get(
            urls=[
                self.individual_server_url.format(server_id=server_id)
                for server_id in server_ids
            ],
            wait_for_class="serverdatadiv",
            delay_between_page_loads=0,
            max_concurrent_requests=10,
            cache_only=True,
        )

        servers = []
        error_list = []
        for server_content in server_pages:
            if not server_content:
                continue

            try:
                server = self._parse_server_content(server_content)
            except Exception as e:
                print(f"Error parsing server content: {e}")
                error_list.append(e)
                continue

            servers.append(server)

        if error_list:
            raise ExceptionGroup(
                "Errors occurred while parsing server content",
                error_list,
            )

        return servers

    def _parse_server_content(self, server_content: str) -> list[FetchedServer]:
        soup = BeautifulSoup(server_content, "html.parser")

        server = FetchedServer()
        server.name = self._parse_server_name(soup)
        server.description = self._parse_server_description(soup)

        server_data_block = soup.select_one("div.serverdatadiv table.serverdata")
        if not server_data_block:
            return server

        server.ip_address_java = server_data_block.find(
            name="th", string="Java IP:"
        ).next_sibling.get_text(strip=True)

        bedrock_ip_header = server_data_block.find(name="th", string="Bedrock IP:")
        if bedrock_ip_header:
            bedrock_ip = bedrock_ip_header.next_sibling.get_text(strip=True)
            bedrock_port = server_data_block.find(
                name="th", string="Bedrock Port:"
            ).next_sibling.get_text(strip=True)
            server.ip_address_bedrock = (
                f"{bedrock_ip}:{bedrock_port}" if bedrock_ip and bedrock_port else None
            )

        server.versions = [
            server_data_block.find(
                name="th", string="Server Version:"
            ).next_sibling.get_text(strip=True)
        ]
        players_str = server_data_block.find(
            name="th", string="Players Online:"
        ).next_sibling.get_text(strip=True)
        players_online, max_players = map(
            int, players_str.split(" / ") if " / " in players_str else (players_str, 0)
        )
        server.players_online = players_online
        server.max_players = max_players
        server.added_at = server_data_block.find(
            name="th", string="Submitted:"
        ).next_sibling.get_text(strip=True)

        status_str = (
            server_data_block.find(name="th", string="Server Status:")
            .next_sibling.get_text(strip=True)
            .lower()
        )
        if "online" in status_str:
            server.status = "online"
        elif "offline" in status_str:
            server.status = "offline"
        else:
            server.status = "unknown"

        server.total_votes = int(
            server_data_block.find(
                name="th", string="Votes - all time:"
            ).next_sibling.get_text(strip=True)
        )

        server.country = self._parse_server_country(server_data_block)

        external_links_header = server_data_block.find(
            name="th", string="External Links:"
        )
        if external_links_header:
            external_links = external_links_header.next_sibling

            if external_links:
                website_link = external_links.find("a", string="Server Website")
                if website_link:
                    server.website = website_link["href"]

                discord_link = external_links.find("a", string="Discord")
                if discord_link:
                    server.discord = discord_link["href"]

        server.tags = self._parse_server_tags(soup)

        return server

    def _parse_server_name(self, soup: BeautifulSoup) -> str:
        name_block = soup.select_one(
            "h1.server-heading.entry-title.server-detail-heading"
        )

        if name_block:
            # The server name is inside an <h1> tag
            # and can be either directly in the tag or in a <a> tag without "button-server-ip" class inside it
            for child in name_block.children:
                if child.name == "a" and "button-server-ip" not in child.get(
                    "class", []
                ):
                    return child.get_text(strip=True)
                elif child.name is None and child.strip():
                    # If the child is a NavigableString, it contains the server name directly
                    return child.strip()
        return ""

    def _parse_server_description(self, soup: BeautifulSoup) -> str:
        description_block = soup.select_one("div.entry-content")

        if not description_block:
            return ""

        description_block_contents = description_block.contents

        start_description_index = None

        description_str = ""

        for i in range(len(description_block_contents)):

            # Description is either in the first <p> tag or contained between 2 empty <p> tags
            if start_description_index is not None:
                # If we have found the start index, we concatenate the text until we find the next <p> tag
                if (
                    description_block_contents[i].name
                    and description_block_contents[i].name != "div"
                ):
                    description_str += description_block_contents[i].get_text(
                        strip=True
                    )

                elif description_block_contents[i].name is None:
                    description_str += str(description_block_contents[i]).strip() + "\n"

            if description_block_contents[i].name == "p":
                description = description_block_contents[i].get_text(strip=True)

                if description:
                    return description

                # If we find an empty <p> tag and it's the first one,
                # we set the start index to capture the description later
                if start_description_index is None:
                    start_description_index = i

                # If we find a second empty <p> tag, we capture the description
                else:
                    return description_str.strip()  # Remove the last newline character

    def _parse_server_country(self, server_data_block: BeautifulSoup) -> str:
        country_block = server_data_block.find(name="th", string="Country:")
        if not country_block:
            return None

        country_flag_block = country_block.next_sibling
        if not country_flag_block:
            return None

        country_flag = country_flag_block.find("img", class_="flag")
        # Extract the country code from the image's alt attribute
        if not country_flag:
            return None

        country_name = country_flag.get("alt", "").strip()
        if country_name:
            if len(country_name) == 2:
                # If the country name is already a 2-letter code, return it directly
                return country_name.lower()

            return get_country_code(country_name)

        return None

    def _parse_server_tags(self, soup: BeautifulSoup) -> list[ServerTag]:
        tag_container = soup.select_one("div.category-container")
        if not tag_container:
            return []
        tags = []
        for tag in tag_container.select("a"):
            tag_name = tag.get_text(strip=True)
            if tag_name:
                tags.append(ServerTag(name=tag_name))

        return tags
