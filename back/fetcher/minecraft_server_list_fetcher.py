from fetcher.helpers.webpage_getter import WebpageGetter
from fetcher.server_fetcher_base import ServerFetcherBase
from core.models import Server
from bs4 import BeautifulSoup


class MinecraftServerListFetcher(ServerFetcherBase):
    server_list_url = "https://minecraft-server-list.com/page/{page_number}/"
    individual_server_url = "https://minecraft-server-list.com/server/{server_id}/"
    max_page_number = 300

    def __init__(self):
        pass

    async def get_new_servers(self) -> list[Server]:
        raise NotImplementedError("Subclasses must implement this.")

    async def get_all_servers(self) -> list[Server]:

        # return []
        # # Returns 403

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
            max_concurrent_requests=5,
        )

        # Parse the content to extract server list
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

        # For each server in the list:
        # Get server details webpage content from the individual server URL
        # Parse the content to extract server details
        # Create a Server object

        await webpage_getter.get(
            urls=[
                self.individual_server_url.format(server_id=server_id)
                for server_id in server_ids
            ],
            wait_for_class="serverdatadiv",
            delay_between_page_loads=0,
            max_concurrent_requests=5,
        )

        # soup = BeautifulSoup(server_content, "html.parser")
        # details_table = soup.select_one("#servertable")
        # if not details_table:
        #     print(f"Server details table not found for server ID: {server_id}")
        #     continue

        # Return the list of servers

        return []
