import os

from fetcher.minecraft_server_list_fetcher import MinecraftServerListFetcher


def test_simple_server_info_parsing():
    content = _load_file("436034")

    fetcher = MinecraftServerListFetcher()
    server = fetcher._parse_server_content(content)

    assert server is not None
    assert server.name == "YourTown Survival"
    assert (
        server.description
        == "Community-minded server with a family-friendly atmosphere! Come join us in the quest for survival, with perks like land claims, rollback protection, anti-grief and other server protections. Attentive staff and friendly playerbase help to make for a positive experience. Come and build your town, with us!"
    )

    assert server.ip_address_java == "mc.yourtown.city"
    assert server.ip_address_bedrock == None
    assert server.banner == (
        "https://cdn.minecraft-server-list.com/serverlogo/436034.jpg"
    )
    assert server.versions == ["1.12.2"]
    assert server.players_online == 0
    assert server.max_players == 3
    assert server.added_at == "2019-02-04 23:12:54"
    assert server.status == "online"
    assert server.total_votes == 811
    assert server.country == "us"
    assert server.website == None
    assert server.discord == None
    assert [tag.name for tag in server.tags] == [
        "Survival",
        "Semi Vanilla",
        "PVP",
        "Land Claim",
    ]


def test_complex_server_info_parsing():
    content = _load_file("380867")

    fetcher = MinecraftServerListFetcher()
    server = fetcher._parse_server_content(content)

    assert server is not None
    assert server.name == "OPBlocks"
    assert (
        server.description
        == """[1.21] OPBlocks is a high-quality Minecraft Prison, Skyblock, Cobblemon/Pixelmon, and Survival SMP server featuring unique content and an amazing community, friendly staff, and awesome players like you!

BEDROCK SUPPORTED!

The Original Candy Prison
Fully Custom Skyblock
Unique Survival SMP
Parkour
Boss Fights
Mob Armor
Dungeons
Quests
Daily Challenges"""
    )

    assert server.banner == (
        "https://cdn.minecraft-server-list.com/serverlogo/380867.jpg"
    )
    assert server.ip_address_java == "fun.opblocks.com"
    assert server.ip_address_bedrock == "bedrock.opblocks.com:19132"
    assert server.versions == ["1.21"]
    assert server.players_online == 737
    assert server.max_players == 3000
    assert server.added_at == "2016-11-15 19:08:57"
    assert server.status == "online"
    assert server.total_votes == 1485920
    assert server.country == "us"
    assert server.website == "https://opblocks.com/"
    assert server.discord == "https://discord.com/invite/tXPUtSPTMN"
    assert [tag.name for tag in server.tags] == [
        "Crossplay",
        "Survival",
        "Pixelmon",
        "Cobblemon",
        "Bedwars",
        "Skywars",
        "Skyblock",
    ]


def _load_file(server_id: str) -> str:
    test_file_name = f"https___minecraft-server-list_com_server_{server_id}_.cache.test"
    test_file = os.path.join(os.path.dirname(__file__), "test_files", test_file_name)

    if not os.path.exists(test_file):
        raise FileNotFoundError(
            f"Test file {test_file} does not exist. Please run the fetcher first."
        )

    with open(test_file, "r", encoding="utf-8") as file:
        content = file.read()
    return content
