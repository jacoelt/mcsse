import asyncio
import logging

from django.core.management.base import BaseCommand

from fetcher.reconciler import update_player_counts
from fetcher.sources import get_all_fetchers

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Quick update of player counts from all sources"

    def handle(self, *args, **options):
        fetchers = get_all_fetchers()
        self.stdout.write(f"Updating player counts from {len(fetchers)} source(s)...")

        all_counts = asyncio.run(self._fetch_counts(fetchers))

        self.stdout.write(f"Fetched {len(all_counts)} player count entries")

        updated = update_player_counts(all_counts)
        self.stdout.write(
            self.style.SUCCESS(f"Done: {updated} servers updated")
        )

    async def _fetch_counts(self, fetchers):
        results = []
        for fetcher in fetchers:
            try:
                count = 0
                async for pc in fetcher.fetch_player_counts():
                    results.append((fetcher.source_name, pc))
                    count += 1
                logger.info(f"{fetcher.source_name}: fetched {count} player counts")
            except Exception:
                logger.exception(
                    f"Error fetching player counts from {fetcher.source_name}"
                )
        return results
