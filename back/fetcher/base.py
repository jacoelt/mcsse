from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import AsyncGenerator, Optional
from urllib.parse import urlparse


def redirected_off_page(requested_url: str, final_url) -> bool:
    """True if following redirects took us off the requested page.

    Many listing sites 30x-redirect past-the-end pagination requests to the
    homepage, which (with follow_redirects=True) returns 200 + valid-looking
    rows. Compare path + query to detect this and stop paginating.
    """
    expected = urlparse(requested_url)
    actual = urlparse(str(final_url))
    return (expected.path, expected.query) != (actual.path, actual.query)


@dataclass
class FetchedServer:
    external_id: str
    name: str
    ip_address: str = ""
    port: int = 25565
    description: str = ""
    game_version: str = ""
    edition: str = "java"
    online_players: int = 0
    max_players: int = 0
    votes: int = 0
    country: str = ""
    tags: list[str] = field(default_factory=list)
    website_url: str = ""
    discord_url: str = ""
    banner_url: str = ""
    is_online: bool = False
    source_url: str = ""


@dataclass
class PlayerCount:
    external_id: str
    online_players: int
    is_online: bool


class ServerFetcher(ABC):
    source_name: str = ""
    priority: int = 99
    base_url: str = ""

    @abstractmethod
    async def fetch_servers(self) -> AsyncGenerator[FetchedServer, None]:
        yield  # type: ignore

    async def fetch_player_counts(self) -> AsyncGenerator[PlayerCount, None]:
        async for server in self.fetch_servers():
            yield PlayerCount(
                external_id=server.external_id,
                online_players=server.online_players,
                is_online=server.is_online,
            )
