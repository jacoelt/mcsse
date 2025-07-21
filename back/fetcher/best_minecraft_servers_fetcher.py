from fetcher.webpage_getter import WebpageGetter
from fetcher.server_fetcher_base import ServerFetcherBase
from core.models import Server
from bs4 import BeautifulSoup


class BestMinecraftServersFetcher(ServerFetcherBase):
    server_list_url = "https://best-minecraft-servers.co/pg.{page_number}"
    individual_server_url = (
        "https://best-minecraft-servers.co/server-complex-gaming.{server_id}"
    )
    max_page_number = 2586

    def __init__(self):
        pass

    async def get_new_servers(self) -> list[Server]:
        raise NotImplementedError("Subclasses must implement this.")

    async def get_all_servers(self) -> list[Server]:

        return []
        # Client connection closed when too many requests are made

        # Get server list webpage content
        server_list_webpage_getter = WebpageGetter(
            url=self.server_list_url,
            max_page_number=self.max_page_number,
        )
        print("Fetching pages content...")
        pages_content = await server_list_webpage_getter.get()

        # Parse the content to extract server list
        server_ids = []
        for page_content in pages_content:
            soup = BeautifulSoup(page_content, "html.parser")
            server_links = soup.select("TBD")

            for link in server_links:
                # Extract server ID from the link
                href = link.get("href", "")
                if href:
                    server_id = href.split("/")[-2]
                    server_ids.append(server_id)
                else:
                    print("No href found in the server link, skipping.")

        # for server_id in server_ids:
        #     # For each server in the list:
        #     # Get server details webpage content from the individual server URL
        #     # Parse the content to extract server details
        #     # Create a Server object
        #     server_url = self.individual_server_url.format(server_id=server_id)
        #     server_webpage_getter = WebpageGetter(url=server_url)
        #     server_content = await server_webpage_getter.get()

        #     soup = BeautifulSoup(server_content, "html.parser")
        #     details_table = soup.select_one("#servertable")
        #     if not details_table:
        #         print(f"Server details table not found for server ID: {server_id}")
        #         continue

        # Return the list of servers

        return []
