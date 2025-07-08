import asyncio
from datetime import date
import aiohttp
from fetcher.server_fetcher_base import ServerFetcherBase
from core.models import Server, ServerTag


PAGE_SIZE = 100


class FindMcServerFetcher(ServerFetcherBase):
    website_url = "https://findmcserver.com/servers"

    list_api_url = "https://findmcserver.com/api/servers"
    server_details_api_url = "https://findmcserver.com/api/servers/{server_id}"

    def __init__(self):
        pass

    async def get_new_servers(self) -> list[Server]:
        pass

    async def get_all_servers(self) -> list[Server]:

        return []
        # Returns 403

        # Fetch all servers from the API
        conn = aiohttp.TCPConnector(limit=10)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0"
        }
        jar = aiohttp.CookieJar(unsafe=True)
        async with aiohttp.ClientSession(
            connector=conn,
            headers=headers,
            cookie_jar=jar,
        ) as session:
            server_slugs = await self._get_server_slug_list(session)

            tasks = []

            async with asyncio.TaskGroup() as tg:
                for slug in server_slugs[:5]:
                    tasks.append(
                        tg.create_task(self._get_server_details(session, slug))
                    )

        servers = [task.result() for task in tasks]
        return servers

    async def _get_server_slug_list(self, session):
        server_slugs = []
        current_page = 0

        while True:
            url = f"{self.list_api_url}?pageNumber={current_page}&pageSize={PAGE_SIZE}"
            print(f"Fetching server list from: {url}")
            async with session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch server list: {response.status}")
                data = await response.json()
                if not data or "data" not in data:
                    break

            total_servers = data.get("count", 0)
            current_server_page = data.get("data", [])
            server_slugs += [server["slug"] for server in current_server_page]

            current_page += 1

            if current_page * PAGE_SIZE > total_servers:
                break

        return server_slugs

    async def _get_server_details(self, session, slug):
        print(f"Fetching details for server: {slug}")

        tags = []

        async with session.get(
            self.server_details_api_url.format(server_id=slug)
        ) as response:
            if response.status != 200:
                raise Exception(
                    f"Failed to fetch server details for {slug}: {response.status}"
                )
            data = await response.json()

        # Create a Server instance from the fetched data
        server = Server(
            name=data["name"],
            ip_address_java=f"{data['javaAddress']}:{data.get('javaPort', 25565)}",
            ip_address_bedrock=f"{data.get('bedrockAddress', '')}:{data.get('bedrockPort', '')}",
            versions=", ".join(version["name"] for version in data.get("version", [])),
            players_online=data["currentOnlinePlayers"],
            max_players=data["currentMaxPlayers"],
            description=data["longDescription"],
            banner=data["iconImage"]["url"] if data.get("iconImage") else None,
            added_at=date.fromisoformat(data["launchedOn"]),
            status="online" if data["isOnline"] else "offline",
            total_votes=data["votes"],
        )

        tags = TagMapper.map_tags(data.get("serverTags", []))

        server.tags.set(tags)

        return server


class TagMapper:
    name_mapping = {
        "CLAN-WARS": "Clan Wars",
        "CLANS": "Clans",
    }

    @staticmethod
    def map_tags(tag_data):
        tags = []
        for tag in tag_data:
            name = TagMapper.name_mapping.get(tag["name"], tag["name"].capitalize())
            description = tag.get("description", "")
            relevance = 0

            tags.append(
                ServerTag(
                    name=name,
                    description=description,
                    relevance=relevance,
                )
            )
        return tags


# {
#   "name": "Block4Block",
#   "slug": "block4block",
#   "iconImage": {
#     "id": "82a8ee2f-2696-45ef-91a3-1a620992fd84",
#     "url": "https://mc-server-listing.s3.amazonaws.com/13c40280-d640-4822-b92b-32f69a943861.webp",
#     "altText": "Server Icon",
#     "title": "Server Icon"
#   },
#   "shortDescription": "You need a block to break a block.",
#   "currentOnlinePlayers": 0,
#   "currentMaxPlayers": 20,
#   "isOnline": true,
#   "serverTags": [
#     {
#       "id": "7bfcbe1d-5a25-4786-b03f-c71a33c29ee5",
#       "name": "CLAN-WARS",
#       "description": "Minecraft \"Clan Wars\" servers have PvP-focused gameplay where different player clans compete against each other",
#       "type": "KEYWORD",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.554"
#     },
#     {
#       "id": "88103e02-215a-4859-92cc-5ccc5e8daa05",
#       "name": "CLANS",
#       "description": "\"Clans\" can be competitive or casual but involve Minecraft players joining or creating virtual clans or factions",
#       "type": "KEYWORD",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.557"
#     },
#   ],
#   "serverLanguage": [
#     {
#       "id": "4572a1c6-42b8-4811-b587-e815df521c38",
#       "name": "ENGLISH",
#       "description": "ENGLISH",
#       "type": "LANGUAGE",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.579"
#     }
#   ],
#   "serverLocation": [
#     {
#       "id": "77c64c32-e53b-4b88-b957-81031e52cd53",
#       "name": "CHINA",
#       "description": "CHINA",
#       "type": "LOCATION",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.582"
#     },
#     {
#       "id": "5fb92a95-93e4-4ed4-ac40-880a032c5bc9",
#       "name": "JAPAN",
#       "description": "JAPAN",
#       "type": "LOCATION",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.585"
#     },
#     {
#       "id": "d261a946-5e22-4a9b-a191-eafc381b31e4",
#       "name": "KOREA",
#       "description": "KOREA",
#       "type": "LOCATION",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.587"
#     },
#     {
#       "id": "39e12267-20b7-464a-8e0e-c9f7f11007e0",
#       "name": "PHILIPPINES",
#       "description": "PHILIPPINES",
#       "type": "LOCATION",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.59"
#     },
#     {
#       "id": "3ecd9d34-377a-4511-b250-8bf8e906ac68",
#       "name": "SINGAPORE",
#       "description": "SINGAPORE",
#       "type": "LOCATION",
#       "is_highlighted": false,
#       "created_at": "2025-04-15T14:47:39.593"
#     }
#   ],
#   "serverMedias": [
#     {
#       "url": "hasjamon@outlook.com",
#       "description": "hasjamon@outlook.com",
#       "social_media": "EMAIL"
#     },
#     {
#       "url": "https://www.b4block.org",
#       "description": "https://www.b4block.org",
#       "social_media": "WEBSITE"
#     },
#     {
#       "url": "https://ko-fi.com/hasjamon/commissions",
#       "description": "https://ko-fi.com/hasjamon/commissions",
#       "social_media": "STORE"
#     },
#     {
#       "url": "https://discord.gg/qAmyTsQxSm",
#       "description": "https://discord.gg/qAmyTsQxSm",
#       "social_media": "DISCORD"
#     },
#     {
#       "url": "https://web-cdn.bsky.app/profile/hasjamon.bsky.social",
#       "description": "https://web-cdn.bsky.app/profile/hasjamon.bsky.social",
#       "social_media": "BLUESKY"
#     }
#   ],
#   "longDescription": "# **Welcome**\nOn **B4Block.org** we are developing a new game mode, a strict version of Minecraft that balances griefing and enables basebuilding PvP.\n\n## **Get started!**\nThe gist; you need a block to break a block. \n\nDiscover and utilize Minecraft's mechanics to indirectly break blocks and obtain them.\n\nMaster Block4Block by refering to your Advancements (Press \"L\" in game). There are two new advancement trees to progress through.\n\n## **Claim the Land!**\nTo make a claim you need a Lectern and a Book and Quill. \n&gt;1. Put the book into the lectern to make a claim.\n&gt;2. All players whose names are in the book share ownership.\n&gt;3. Claims are protected by the immediate surrounding blocks (expect for above, below and diagonally).\n&gt;4. Claims make non-members unable to place blocks within them, as well as prevent the use of utilities such as buckets. \n&gt;5. Claims allow members to break certain blocks freely within the claim, for example blocks used for redstone contraptions. When you unsuccessfully attempt to break a block, it will tell you if you can break it freely within a claim.\n&gt;6. Steal a claimbook from it's lectern to lift the claim and add your name to claim it as your own.\n\n*Beware: non-members can still break blocks, costing a block like everywhere else.*\n\n## **Contribute to the Development**\nThe project is Open Source and files can be found on Spigotmc, Modrinth and PlanetMinecraft, as well as Github.\n\nContribute to the development on Discord: https://discord.gg/rNena844ya",
#   "javaAddress": "play.b4block.org",
#   "javaPort": 25565,
#   "bedrockAddress": null,
#   "bedrockPort": null,
#   "launchedOn": "2021-07-21T16:00:00.000Z",
#   "version": [
#     {
#       "id": "6b11e20e-e653-4995-841f-74ae12574c22",
#       "name": "1.21.5",
#       "description": "1.21.5",
#       "type": "VERSION",
#       "is_highlighted": true,
#       "created_at": "2025-04-15T14:47:39.553103"
#     }
#   ],
#   "votes": 50,
# }
