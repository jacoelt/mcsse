import asyncio
from django.core.management.base import BaseCommand

from fetcher import fetch


class Command(BaseCommand):
    help = "Fetch all Minecraft servers"

    def handle(self, *args, **kwargs):
        asyncio.run(fetch.run())
        self.stdout.write(
            self.style.SUCCESS("Successfully fetched all Minecraft servers")
        )
