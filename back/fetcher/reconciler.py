import logging
from collections import defaultdict
from datetime import datetime, timezone

from django.utils.text import slugify

from core.models import Server, ServerSource, Tag

from .base import FetchedServer

logger = logging.getLogger(__name__)

# Priority order: lower number = higher priority
SOURCE_PRIORITY = {
    "minecraft-mp": 1,
    "minecraftservers-org": 2,
    "minecraft-server-list": 3,
    "planetminecraft": 4,
    "best-minecraft-servers": 5,
    "findmcserver": 6,
    "topg": 7,
    "minecraft-buzz": 8,
    "serveur-minecraft": 9,
}


def reconcile_servers(fetched: list[tuple[str, FetchedServer]]):
    """
    Takes a list of (source_name, FetchedServer) tuples.
    Groups by ip:port (or name fallback), merges, and upserts into DB.
    """
    groups: dict[str, list[tuple[str, FetchedServer]]] = defaultdict(list)

    for source_name, server in fetched:
        if server.ip_address:
            key = f"{server.ip_address}:{server.port}"
        else:
            key = f"name:{server.name.lower().strip()}"
        groups[key].append((source_name, server))

    created_count = 0
    updated_count = 0

    for key, entries in groups.items():
        # Sort by source priority (lowest number = highest priority)
        entries.sort(key=lambda e: SOURCE_PRIORITY.get(e[0], 99))

        merged = _merge_entries(entries)
        db_server, was_created = _upsert_server(key, merged, entries)

        if was_created:
            created_count += 1
        else:
            updated_count += 1

        _upsert_sources(db_server, entries)
        _sync_tags(db_server, merged["tags"])

    logger.info(f"Reconciled: {created_count} created, {updated_count} updated")
    return created_count, updated_count


def _merge_entries(
    entries: list[tuple[str, FetchedServer]],
) -> dict:
    """Merge multiple source entries into a single dict of field values."""
    result: dict = {
        "name": "",
        "ip_address": "",
        "port": 25565,
        "description": "",
        "game_version": "",
        "edition": "java",
        "online_players": 0,
        "max_players": 0,
        "votes": 0,
        "country": "",
        "website_url": "",
        "discord_url": "",
        "banner_url": "",
        "is_online": False,
        "tags": set(),
    }

    total_votes = 0
    best_description = ""
    latest_players = (None, 0, 0, False)  # (timestamp, online, max, is_online)

    # Entries are already sorted by priority (highest first)
    for source_name, server in entries:
        # Priority fields: use first non-empty value (highest priority)
        for field_name in [
            "name",
            "ip_address",
            "port",
            "game_version",
            "edition",
            "country",
            "website_url",
            "discord_url",
            "banner_url",
        ]:
            current = result[field_name]
            value = getattr(server, field_name)
            if not current and value:
                result[field_name] = value

        # Votes: sum across all sources
        total_votes += server.votes

        # Description: use the longest
        if len(server.description) > len(best_description):
            best_description = server.description

        # Players: use the value (all fetched roughly at the same time)
        if server.online_players > result["online_players"]:
            result["online_players"] = server.online_players
            result["max_players"] = server.max_players
            result["is_online"] = server.is_online

        # Tags: union
        for tag in server.tags:
            result["tags"].add(tag.lower().strip())

    result["votes"] = total_votes
    result["description"] = best_description

    return result


def _upsert_server(
    key: str,
    merged: dict,
    entries: list[tuple[str, FetchedServer]],
) -> tuple[Server, bool]:
    """Find or create a Server record, then update its fields."""
    lookup = {}
    if not key.startswith("name:"):
        ip, port_str = key.rsplit(":", 1)
        lookup = {"ip_address": ip, "port": int(port_str)}
    else:
        lookup = {"name__iexact": key[5:]}

    try:
        server = Server.objects.get(**lookup)
        was_created = False
    except Server.DoesNotExist:
        server = Server()
        was_created = True
    except Server.MultipleObjectsReturned:
        server = Server.objects.filter(**lookup).first()
        was_created = False

    server.name = merged["name"] or server.name
    server.ip_address = merged["ip_address"] or server.ip_address
    server.port = merged["port"] or server.port
    server.description = merged["description"] or server.description
    server.game_version = merged["game_version"] or server.game_version
    server.edition = merged["edition"] or server.edition
    server.online_players = merged["online_players"]
    server.max_players = merged["max_players"]
    server.votes = merged["votes"]
    server.country = merged["country"] or server.country
    server.website_url = merged["website_url"] or server.website_url
    server.discord_url = merged["discord_url"] or server.discord_url
    server.banner_url = merged["banner_url"] or server.banner_url
    server.is_online = merged["is_online"]
    server.last_checked = datetime.now(timezone.utc)
    server.save()

    return server, was_created


def _upsert_sources(
    server: Server,
    entries: list[tuple[str, FetchedServer]],
):
    """Create or update ServerSource records for each source."""
    for source_name, fetched in entries:
        ServerSource.objects.update_or_create(
            source_name=source_name,
            external_id=fetched.external_id,
            defaults={
                "server": server,
                "source_url": fetched.source_url,
                "raw_data": {
                    "name": fetched.name,
                    "ip_address": fetched.ip_address,
                    "port": fetched.port,
                    "description": fetched.description[:500],
                    "game_version": fetched.game_version,
                    "edition": fetched.edition,
                    "online_players": fetched.online_players,
                    "max_players": fetched.max_players,
                    "votes": fetched.votes,
                    "country": fetched.country,
                    "tags": fetched.tags,
                },
            },
        )


def _sync_tags(server: Server, tag_names: set[str]):
    """Sync the server's tags M2M from a set of tag name strings."""
    if not tag_names:
        return

    tag_objects = []
    for tag_name in tag_names:
        slug = slugify(tag_name)
        if not slug:
            continue
        tag, _ = Tag.objects.get_or_create(
            name=slug,
            defaults={"display_name": tag_name.title()},
        )
        tag_objects.append(tag)

    server.tags.set(tag_objects)


def update_player_counts(counts: list[tuple[str, "PlayerCount"]]):
    """Bulk update player counts from hourly fetch."""
    from .base import PlayerCount

    updated = 0
    for source_name, pc in counts:
        try:
            source = ServerSource.objects.select_related("server").get(
                source_name=source_name,
                external_id=pc.external_id,
            )
        except ServerSource.DoesNotExist:
            continue

        server = source.server
        server.online_players = pc.online_players
        server.is_online = pc.is_online
        server.last_checked = datetime.now(timezone.utc)
        server.save(update_fields=["online_players", "is_online", "last_checked", "updated_at"])
        updated += 1

    logger.info(f"Updated player counts for {updated} servers")
    return updated
