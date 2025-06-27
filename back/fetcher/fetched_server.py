class FetchedServer:
    """Represents a Minecraft server fetched from a server list."""

    name: str = None
    description: str = None
    ip_address_java: str = None
    ip_address_bedrock: str = None
    versions: list[str] = []
    players_online: int = 0
    max_players: int = 0
    banner: str = None
    added_at: str = None
    status: str = None
    total_votes: int = 0
    country: str = None
    languages: list[str] = []
    website: str = None
    discord: str = None
    tags: list[str] = []
