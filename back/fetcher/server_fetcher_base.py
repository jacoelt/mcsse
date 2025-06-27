from fetcher.fetched_server import FetchedServer


class ServerFetcherBase:

    def __init__(self):
        raise NotImplementedError("Not to be instanciated directly.")

    async def get_all_servers(self) -> list[FetchedServer]:
        raise NotImplementedError("Subclasses must implement this.")
