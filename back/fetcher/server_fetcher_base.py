from core.models import Server


class ServerFetcherBase:

    def __init__(self):
        raise NotImplementedError("Not to be instanciated directly.")

    async def get_new_servers(self) -> list[Server]:
        raise NotImplementedError("Subclasses must implement this.")

    async def get_all_servers(self) -> list[Server]:
        raise NotImplementedError("Subclasses must implement this.")
