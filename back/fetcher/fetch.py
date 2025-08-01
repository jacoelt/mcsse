import asyncio
import logging

from django.conf import settings
from django.db import transaction

from fetcher.fetched_server import FetchedServer
from core.models import Server, ServerTag
from asgiref.sync import sync_to_async

from fetcher.minecraft_server_list_fetcher import MinecraftServerListFetcher
from fetcher.minecraftservers_fetcher import MinecraftServersFetcher


logger = logging.getLogger(__name__)


WEBSITE_STRATEGIES = [
    # Sequence order is important, later servers will override earlier ones with more accurate data.
    # MinecraftBuzzFetcher,  # "https://minecraft.buzz/"
    MinecraftServerListFetcher,  # "https://minecraft-server-list.com/"
    # MinecraftMpFetcher,  # "https://minecraft-mp.com/"
    # ServerFetcherBase,  # "https://www.planetminecraft.com/servers/"
    # ServerFetcherBase,  # "https://topg.org/Minecraft-servers"
    MinecraftServersFetcher,  # "https://minecraftservers.org/"
    # ServerFetcherBase,  # "https://serveur-minecraft.com/"
    # FindMcServerFetcher,  # "https://findmcserver.com/servers"
    # BestMinecraftServersFetcher,  # "https://best-minecraft-servers.co/"
]


async def run(do_save: bool = True):
    logger.info("Starting the fetching process...")

    is_first_run = True

    all_existing_ids = set()

    for strategyKlass in WEBSITE_STRATEGIES:
        logger.info(f"Getting server list from {strategyKlass.__name__}...")
        strategy = strategyKlass()

        try:
            servers = await strategy.get_all_servers()
            logger.info(
                f"Fetched {len(servers)} servers from {strategyKlass.__name__}."
            )
        except Exception as e:
            logger.warning(f"Error fetching servers from {strategyKlass.__name__}")
            logger.exception(e)
            continue

        logger.info(
            f"Saving servers and tags to the database for {strategyKlass.__name__}..."
        )

        if not do_save:
            logger.info("Skipping saving of data as per command line argument.")
            continue

        if settings.DEBUG:
            from django.db import connection

            query_count = len(connection.queries)

        existing_ids = await sync_to_async(save_to_database)(
            servers, is_first_run=is_first_run
        )
        all_existing_ids.update(existing_ids)

        is_first_run = False

        if settings.DEBUG:
            logger.info(
                f"Saved servers and tags to the database. Total queries made: {len(connection.queries) - query_count}."
            )

    logger.info("Fetching process completed.")

    if all_existing_ids:
        logger.info("Remove servers that are no longer in the database...")
        await sync_to_async(remove_stale_servers)(all_existing_ids)

    logger.info(f"Done.")


def save_to_database(
    fetched_server_list: list[FetchedServer],
    is_first_run: bool = False,
) -> list[str]:
    # Multiple step process:
    # 1. Save all tags first to ensure they exist in the database.
    # 2. Split servers into those that need to be created and those that need to be updated.
    # 3. Create new servers and update existing ones, without changing tags, with batch operations.
    # 4. Add tags to the servers after they are created or updated.

    servers_ips = set()

    # 1. Save all tags first to ensure they exist in the database.
    tags_mapping = {tag.name: tag for tag in ServerTag.objects.all()}

    for fetched_server in fetched_server_list:
        if (
            not fetched_server.name
            or fetched_server.name.strip() == ""
            or (
                fetched_server.ip_address_java is None
                and fetched_server.ip_address_bedrock is None
            )
        ):
            logger.warning("Skipping server with no name.")
            continue

        tags_to_create = []

        for tag in fetched_server.tags:
            if tag.name not in tags_mapping:
                logger.info(f"Saving new tag: {tag.name}")
                tags_to_create.append(tag)

        if tags_to_create:
            created_tags = ServerTag.objects.bulk_create(
                tags_to_create, ignore_conflicts=True
            )
            for created_tag in created_tags:
                tags_mapping[created_tag.name] = created_tag

        servers_ips.add(
            (fetched_server.ip_address_java, fetched_server.ip_address_bedrock)
        )

    # 2. Split servers into those that need to be created and those that need to be updated.
    # Get list of servers that already exist in the database
    existing_servers_mapping = {
        (
            server_from_db.ip_address_java,
            server_from_db.ip_address_bedrock,
        ): server_from_db
        for server_from_db in Server.objects.all().prefetch_related("tags")
    }

    # Split servers into those that need to be created and those that need to be updated
    fetched_servers_to_create = []
    fetched_servers_to_update = []
    for fetched_server in fetched_server_list:
        if (
            not fetched_server.name
            or fetched_server.name.strip() == ""
            or (
                fetched_server.ip_address_java is None
                and fetched_server.ip_address_bedrock is None
            )
        ):
            logger.warning("Skipping server with no name.")
            continue

        if (
            fetched_server.ip_address_java,
            fetched_server.ip_address_bedrock,
        ) in existing_servers_mapping:
            logger.debug(f"Server {fetched_server.name} already exists, updating.")
            fetched_servers_to_update.append(fetched_server)
        else:
            logger.debug(f"Server {fetched_server.name} does not exist, creating.")
            fetched_servers_to_create.append(fetched_server)

    # 3. Create new servers and update existing ones, without changing tags, with batch operations.
    if fetched_servers_to_create:
        logger.info(f"Creating {len(fetched_servers_to_create)} new servers.")
        created_servers = Server.objects.bulk_create(
            [
                Server.from_fetched_server(server)
                for server in fetched_servers_to_create
            ],
            ignore_conflicts=True,
        )
        for i, created_servers in enumerate(created_servers):
            fetched_servers_to_create[i].id = created_servers.id

    if fetched_servers_to_update:
        logger.info(f"Updating {len(fetched_servers_to_update)} existing servers.")

        updated_servers = []
        for fetched_server in fetched_servers_to_update:
            server_from_db = existing_servers_mapping.get(
                (fetched_server.ip_address_java, fetched_server.ip_address_bedrock)
            )
            if server_from_db:
                server_from_db.updateData(
                    fetched_server,
                    should_reset_total_votes=is_first_run,
                )
                updated_servers.append(server_from_db)

        Server.objects.bulk_update(
            updated_servers,
            Server.list_of_updated_fields,
            batch_size=1000,
        )

        for i, updated_server in enumerate(updated_servers):
            fetched_servers_to_update[i].id = updated_server.id

    # 4. Add tags to the servers after they are created or updated.
    server_tags_join = []
    for fetched_server in fetched_servers_to_create + fetched_servers_to_update:
        if not fetched_server.tags:
            continue
        for tag in fetched_server.tags:
            if tag.name not in tags_mapping:
                logger.warning(f"Tag {tag.name} not found in tags mapping.")
                continue
            tag_from_db = tags_mapping[tag.name]
            server_tags_join.append(
                ServerTag.servers.through(
                    server_id=fetched_server.id,
                    servertag_id=tag_from_db.id,
                )
            )

    with transaction.atomic():
        # Ensure all server-tag relationships are destroyed and created in a single transaction
        ServerTag.servers.through.objects.all().delete()
        ServerTag.servers.through.objects.bulk_create(
            server_tags_join, ignore_conflicts=True
        )

    return {
        fetched_server.id
        for fetched_server in fetched_servers_to_create + fetched_servers_to_update
    }


def remove_stale_servers(existing_ids: set[str]):
    """
    Remove servers that no longer exist on the listings.
    """
    logger.info("Removing stale servers...")

    # Get all servers that are not in the existing_ids set
    stale_servers = Server.objects.exclude(id__in=existing_ids)

    if stale_servers.exists():
        logger.info(f"Found {stale_servers.count()} stale servers to remove.")
        stale_servers.delete()
    else:
        logger.info("No stale servers found.")

    logger.info("Stale servers removal completed.")


if __name__ == "__main__":
    asyncio.run(run())
