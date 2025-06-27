import asyncio
from fetcher.best_minecraft_servers_fetcher import BestMinecraftServersFetcher
from fetcher.find_mc_server_fetcher import FindMcServerFetcher
from fetcher.minecraft_buzz_fetcher import MinecraftBuzzFetcher
from fetcher.minecraft_mp_fetcher import MinecraftMpFetcher
from fetcher.minecraft_server_list_fetcher import MinecraftServerListFetcher
from core.models import Server, ServerTag
from fetcher.minecraftservers_fetcher import MinecraftServersFetcher


WEBSITE_STRATEGIES = [
    # Sequence order is important, later servers will override earlier ones with more accurate data.
    MinecraftBuzzFetcher,  # "https://minecraft.buzz/"
    MinecraftServerListFetcher,  # "https://minecraft-server-list.com/"
    MinecraftMpFetcher,  # "https://minecraft-mp.com/"
    # ServerFetcherBase,  # "https://www.planetminecraft.com/servers/"
    # ServerFetcherBase,  # "https://topg.org/Minecraft-servers"
    MinecraftServersFetcher,  # "https://minecraftservers.org/"
    # ServerFetcherBase,  # "https://serveur-minecraft.com/"
    FindMcServerFetcher,  # "https://findmcserver.com/servers"
    BestMinecraftServersFetcher,  # "https://best-minecraft-servers.co/"
]


async def run():
    print("Starting the fetching process...")

    for strategyKlass in WEBSITE_STRATEGIES:
        print(f"Getting server list from {strategyKlass.__name__}...")
        strategy = strategyKlass()
        server_list = await strategy.get_all_servers()

        print(f"Fetched {len(server_list)} servers.")

        for server in server_list:
            for tag in server.tags.all():
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
                server.save()
            else:
                print(f"Server {server.name} already exists in the database, updating.")
                existing_server.updateData(server)


if __name__ == "__main__":
    asyncio.run(run())
