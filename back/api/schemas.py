from datetime import datetime
from typing import Optional

from ninja import FilterSchema, Schema
from pydantic import Field


class TagSchema(Schema):
    name: str
    display_name: str


class ServerSummarySchema(Schema):
    id: str
    name: str
    game_version: str
    edition: str
    online_players: int
    max_players: int
    votes: int
    country: str
    tags: list[TagSchema]
    banner_url: str
    is_online: bool

    @staticmethod
    def resolve_id(obj):
        return str(obj.id)

    @staticmethod
    def resolve_tags(obj):
        if hasattr(obj, "_prefetched_objects_cache") and "tags" in obj._prefetched_objects_cache:
            return obj.tags.all()
        return obj.tags.all()


class ServerSourceSchema(Schema):
    source_name: str
    source_url: str


class ServerDetailSchema(Schema):
    id: str
    name: str
    ip_address: str
    port: int
    description: str
    game_version: str
    edition: str
    online_players: int
    max_players: int
    votes: int
    country: str
    website_url: str
    discord_url: str
    banner_url: str
    is_online: bool
    tags: list[TagSchema]
    sources: list[ServerSourceSchema]
    created_at: datetime
    updated_at: datetime
    last_checked: Optional[datetime]

    @staticmethod
    def resolve_id(obj):
        return str(obj.id)

    @staticmethod
    def resolve_tags(obj):
        return obj.tags.all()

    @staticmethod
    def resolve_sources(obj):
        return obj.sources.all()


class ServerFilterSchema(FilterSchema):
    q: Optional[str] = Field(None, q="name__icontains")
    version: Optional[str] = Field(None, q="game_version__istartswith")
    edition: Optional[str] = Field(None, q="edition")
    players_min: Optional[int] = Field(None, q="online_players__gte")
    players_max: Optional[int] = Field(None, q="online_players__lte")
    max_players_min: Optional[int] = Field(None, q="max_players__gte")
    max_players_max: Optional[int] = Field(None, q="max_players__lte")
    votes_min: Optional[int] = Field(None, q="votes__gte")
    votes_max: Optional[int] = Field(None, q="votes__lte")
    created_after: Optional[datetime] = Field(None, q="created_at__gte")
    created_before: Optional[datetime] = Field(None, q="created_at__lte")
    country: Optional[str] = Field(None, q="country")


class TagWithCountSchema(Schema):
    name: str
    display_name: str
    count: int


class VersionCountSchema(Schema):
    version: str
    count: int


class CountryCountSchema(Schema):
    country: str
    count: int


class FiltersResponseSchema(Schema):
    versions: list[VersionCountSchema]
    countries: list[CountryCountSchema]
    tags: list[TagWithCountSchema]


class PaginatedResponseSchema(Schema):
    count: int
    page: int
    page_size: int
    results: list[ServerSummarySchema]
