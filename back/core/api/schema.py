from ninja import ModelSchema, Schema

from core.models import Server, ServerTag


class ServerTagOut(ModelSchema):
    class Meta:
        model = ServerTag
        fields = ["name", "description", "relevance"]


class ServerOut(ModelSchema):
    tags: list[ServerTagOut] = []

    class Meta:
        model = Server
        fields = "__all__"


class SearchIn(Schema):
    """
    Schema for searching servers.
    """

    query: str | None = None  # Text search query for name and ip
    versions: list[str] | None = None  # Array of versions to filter by
    edition: str | None = None  # Edition filter
    players_online_min: int | None = None  # Minimum players online
    players_online_max: int | None = None  # Maximum players online
    max_players_min: int | None = None  # Minimum max players
    max_players_max: int | None = None  # Maximum max players
    days_prior: int | None = None  # Days prior to filter by
    statuses: list[str] | None = None  # Server status
    total_votes_min: int | None = None  # Minimum total votes
    total_votes_max: int | None = None  # Maximum total votes
    countries: list[str] | None = None  # Array of countries to filter by
    languages: list[str] | None = None  # Array of languages to filter by
    tags: list[str] | None = None  # Array of tags to filter by
    sort_by: str | None = "name"  # Sort by field
    sort_order: str | None = "asc"  # Sort order
    page: int | None = 1  # Page number for pagination
    page_size: int | None = 10  # Number of results per page
