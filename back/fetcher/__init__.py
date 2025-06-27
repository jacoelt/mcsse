import asyncio
from fetcher.minecraft_server_list_fetcher import MinecraftServerListFetcher
from core.models import Server, ServerTag
from asgiref.sync import sync_to_async


WEBSITE_STRATEGIES = [
    # Sequence order is important, later servers will override earlier ones with more accurate data.
    # MinecraftBuzzFetcher,  # "https://minecraft.buzz/"
    MinecraftServerListFetcher,  # "https://minecraft-server-list.com/"
    # MinecraftMpFetcher,  # "https://minecraft-mp.com/"
    # ServerFetcherBase,  # "https://www.planetminecraft.com/servers/"
    # ServerFetcherBase,  # "https://topg.org/Minecraft-servers"
    # MinecraftServersFetcher,  # "https://minecraftservers.org/"
    # ServerFetcherBase,  # "https://serveur-minecraft.com/"
    # FindMcServerFetcher,  # "https://findmcserver.com/servers"
    # BestMinecraftServersFetcher,  # "https://best-minecraft-servers.co/"
]


async def run():
    print("Starting the fetching process...")

    server_list = []
    for strategyKlass in WEBSITE_STRATEGIES:
        print(f"Getting server list from {strategyKlass.__name__}...")
        strategy = strategyKlass()

        try:
            servers = await strategy.get_all_servers()
            print(f"Fetched {len(servers)} servers from {strategyKlass.__name__}.")
            server_list.extend(servers)
        except Exception as e:
            print(f"Error fetching servers from {strategyKlass.__name__}: {e}")
            continue

    print(f"Fetched {len(server_list)} servers.")

    print("Saving servers and tags to the database...")

    await sync_to_async(save_to_database)(server_list)


def save_to_database(server_list):
    for server in server_list:
        for tag in server.tags:
            if not ServerTag.objects.filter(name=tag.name).exists():
                print(f"Saving new tag: {tag.name}")
                tag.save()

        # Check if the server already exists in the database
        existing_server = Server.objects.filter(
            ip_address_java=server.ip_address_java,
            ip_address_bedrock=server.ip_address_bedrock,
        ).first()

        if not existing_server:
            print(
                f"Saving new server: {server.name} ({server.ip_address_java or server.ip_address_bedrock})"
            )
            existing_server = Server()

        else:
            print(f"Server {server.name} already exists in the database, updating.")

        existing_server.updateData(server)


if __name__ == "__main__":
    asyncio.run(run())
