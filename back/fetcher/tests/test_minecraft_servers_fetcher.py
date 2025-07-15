import os

from fetcher.minecraftservers_fetcher import MinecraftServersFetcher


def test_server_info_parsing_single_ip():
    content = _load_file("651307")

    fetcher = MinecraftServersFetcher()
    server = fetcher._parse_server_content(content)

    assert server is not None
    assert server.name == "CobbleLand"
    assert (
        server.description
        == """Welcome to CobbleLand! Bringing the cobblemon experience to vanilla Minecraft! If you enjoy the survival aspects of Minecraft then you'll have a blast over here!

Our Features:
Land claiming to protect your chests and builds!!
Mega Evolutions
Player Gyms
GTS
Player Shops
New Release of Pokemon
And much more in the making!

Check out our Discord here: https://discord.gg/urwvKkTcm8
Here is our IP: play.cobbleland.com"""
    )

    assert server.ip_address_java == "play.cobbleland.com"
    assert server.ip_address_bedrock == None
    assert server.banner == (
        "https://minecraftservers.org/banners/6513071685939613.gif"
    )
    assert server.versions == ["1.21.4"]
    assert server.players_online == 94
    assert server.max_players == 1000
    assert server.added_at == None
    assert server.status == "online"
    assert server.total_votes == 1264
    assert server.country == "ca"
    assert server.website == "https://store.cobbleland.com/"
    assert server.discord == "https://discord.gg/urwvKkTcm8"
    assert [tag.name for tag in server.tags] == [
        "Cobblemon",
        "Economy",
        "PvE",
        "Survival",
        "Vanilla",
    ]


def test_server_info_parsing_dual_ip():
    content = _load_file("621405")

    fetcher = MinecraftServersFetcher()
    server = fetcher._parse_server_content(content)

    assert server is not None
    assert server.name == "CosmosMC"
    assert (
        server.description
        == """Welcome to CosmosMC. Our server has the friendliest community on Minecraft. We're a Network that offers the best of the best Earth, Survival, Oneblock and factions gamemodes.

We're always innovating and pushing to improve, and all community feedback gets taken into account and implemented. If you the player wants something changed, added, or removed, we make it happen.

Join today to learn all about each gamemodes features!

If connecting on Bedrock Edition, or any version of the game that isn't java follow these instructions.

USE THE IP: org.cosmosmc.org
PORT: 19132
"""
    )

    assert server.ip_address_java == "org.cosmosmc.org"
    assert server.ip_address_bedrock == "org.cosmosmc.org"
    assert server.banner == (
        "https://minecraftservers.org/banners/6214051737311135.gif"
    )
    assert server.versions == ["1.21.7"]
    assert server.players_online == 163
    assert server.max_players == 1000
    assert server.added_at == None
    assert server.status == "online"
    assert server.total_votes == 4330
    assert server.country == "us"
    assert server.website == "https://cosmosmc.org"
    assert server.discord == "https://discord.gg/cosmosmc"
    assert [tag.name for tag in server.tags] == [
        "Earth",
        "Economy",
        "PvP",
        "Skyblock",
        "Survival",
        "Towny",
        "Vanilla",
    ]


def _load_file(server_id: str) -> str:
    test_file_name = f"https___minecraftservers_org_server_{server_id}.cache.test"
    test_file = os.path.join(os.path.dirname(__file__), "test_files", test_file_name)

    if not os.path.exists(test_file):
        raise FileNotFoundError(
            f"Test file {test_file} does not exist. Please run the fetcher first."
        )

    with open(test_file, "r", encoding="utf-8") as file:
        content = file.read()
    return content
