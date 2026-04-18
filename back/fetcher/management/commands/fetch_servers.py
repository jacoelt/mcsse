import asyncio
import logging

from django.core.management.base import BaseCommand

from fetcher.reconciler import reconcile_servers
from fetcher.sources import get_all_fetchers

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetch servers from all sources and reconcile into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=str,
            help="Only fetch from a specific source (e.g. minecraft-mp)",
        )

    def handle(self, *args, **options):
        source_filter = options.get("source")
        fetchers = get_all_fetchers()

        if source_filter:
            fetchers = [f for f in fetchers if f.source_name == source_filter]
            if not fetchers:
                self.stderr.write(f"Unknown source: {source_filter}")
                return

        self.stdout.write(f"Fetching from {len(fetchers)} source(s)...")

        all_fetched = asyncio.run(self._fetch_all(fetchers))

        self.stdout.write(f"Fetched {len(all_fetched)} server entries total")

        created, updated = reconcile_servers(all_fetched)
        self.stdout.write(self.style.SUCCESS(f"Done: {created} created, {updated} updated"))

    async def _fetch_all(self, fetchers):
        results = []
        for fetcher in fetchers:
            try:
                count = 0
                async for server in fetcher.fetch_servers():
                    results.append((fetcher.source_name, server))
                    count += 1
                logger.info(f"{fetcher.source_name}: fetched {count} servers")
            except Exception:
                logger.exception(f"Error fetching from {fetcher.source_name}")
        return results
