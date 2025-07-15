import asyncio
from django.core.management.base import BaseCommand

from fetcher import fetch


class Command(BaseCommand):
    help = "Fetch all Minecraft servers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-save",
            action="store_false",
            dest="do_save",
            default=True,
            help="Skip saving the data",
        )

        parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
            help="Run in debug mode",
        )

    def handle(self, *args, **kwargs):
        do_save = kwargs.get("do_save", True)
        if kwargs.get("debug", False):
            import logging

            logging.basicConfig(level=logging.DEBUG)

        asyncio.run(fetch.run(do_save=do_save))
        self.stdout.write(
            self.style.SUCCESS("Successfully fetched all Minecraft servers")
        )
