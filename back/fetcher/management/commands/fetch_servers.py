import asyncio
import logging

from django.core.management.base import BaseCommand

from fetcher.reconciler import reconcile_servers
from fetcher.sources import get_all_fetchers

logger = logging.getLogger("fetcher")


class Command(BaseCommand):
    help = "Fetch servers from all sources and reconcile into the database"

    def create_parser(self, prog_name, subcommand, **kwargs):
        parser = super().create_parser(prog_name, subcommand, **kwargs)
        # Django binds `-v` to --verbosity. Free it up so we can use -v / -vv as
        # a count flag, while keeping --verbosity as a long-form option.
        for action in list(parser._actions):
            if action.dest == "verbosity":
                for opt in list(action.option_strings):
                    parser._option_string_actions.pop(opt, None)
                action.option_strings = ["--verbosity"]
                parser._option_string_actions["--verbosity"] = action
                break
        parser.add_argument(
            "-v",
            dest="fetch_verbose",
            action="count",
            default=0,
            help="Verbose output: -v for per-page progress, -vv to include transport-level logs",
        )
        return parser

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=str,
            help="Only fetch from a specific source (e.g. minecraft-mp)",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Print progress info for each source (INFO level)",
        )

    def handle(self, *args, **options):
        debug = options.get("debug", False)
        verbose = options.get("fetch_verbose", 0)

        self._configure_logging(debug=debug, verbose=verbose)

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

        logger.info("reconciling %d entries", len(all_fetched))
        created, updated = reconcile_servers(all_fetched)
        self.stdout.write(self.style.SUCCESS(f"Done: {created} created, {updated} updated"))

    def _configure_logging(self, *, debug: bool, verbose: int):
        if not (debug or verbose):
            return

        handler = logging.StreamHandler(self.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%H:%M:%S")
        )

        fetcher_logger = logging.getLogger("fetcher")
        fetcher_logger.addHandler(handler)

        if verbose >= 2:
            # Very verbose: DEBUG everywhere, including transport libs
            root = logging.getLogger()
            root.addHandler(handler)
            root.setLevel(logging.DEBUG)
            fetcher_logger.setLevel(logging.DEBUG)
        elif verbose >= 1:
            # Verbose: DEBUG on fetcher (per-page progress)
            fetcher_logger.setLevel(logging.DEBUG)
        else:
            # --debug: INFO on fetcher (per-source progress)
            fetcher_logger.setLevel(logging.INFO)

    async def _fetch_all(self, fetchers):
        results = []
        for fetcher in fetchers:
            logger.info("%s: starting", fetcher.source_name)
            try:
                count = 0
                async for server in fetcher.fetch_servers():
                    results.append((fetcher.source_name, server))
                    count += 1
                logger.info("%s: fetched %d servers", fetcher.source_name, count)
            except Exception:
                logger.exception("%s: error during fetch", fetcher.source_name)
        return results
