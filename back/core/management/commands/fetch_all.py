import asyncio
from django.core.management.base import BaseCommand

import fetcher


class Command(BaseCommand):
    help = "Fetch all Minecraft servers"

    def handle(self, *args, **kwargs):
        asyncio.run(fetcher.run())
        self.stdout.write(
            self.style.SUCCESS("Successfully fetched all Minecraft servers from FindMC")
        )
