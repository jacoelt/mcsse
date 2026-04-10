from fetcher.base import ServerFetcher

from .best_minecraft_servers import BestMinecraftServersFetcher
from .findmcserver import FindMCServerFetcher
from .minecraft_buzz import MinecraftBuzzFetcher
from .minecraft_mp import MinecraftMPFetcher
from .minecraft_server_list import MinecraftServerListFetcher
from .minecraftservers_org import MinecraftServersOrgFetcher
from .planetminecraft import PlanetMinecraftFetcher
from .serveur_minecraft import ServeurMinecraftFetcher
from .topg import TopGFetcher

ALL_FETCHERS: list[type[ServerFetcher]] = [
    MinecraftMPFetcher,
    MinecraftServersOrgFetcher,
    MinecraftServerListFetcher,
    PlanetMinecraftFetcher,
    BestMinecraftServersFetcher,
    FindMCServerFetcher,
    TopGFetcher,
    MinecraftBuzzFetcher,
    ServeurMinecraftFetcher,
]


def get_all_fetchers() -> list[ServerFetcher]:
    return [cls() for cls in ALL_FETCHERS]
