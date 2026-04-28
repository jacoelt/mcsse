from bs4 import BeautifulSoup
from django.test import SimpleTestCase

from fetcher.sources.planetminecraft import PlanetMinecraftFetcher


class PlanetMinecraftSentinelTest(SimpleTestCase):
    """65535 (0xFFFF) is the protocol "unknown" sentinel; planetminecraft renders
    it literally (e.g. "65,535/100"). Treat it as no-signal so the reconciler
    falls through to a real source. Regression test for issue #11."""

    def _item(self, status_text: str):
        html = f"""
        <li class="resource_server_item">
          <a class="server-title" href="/server/test-server/" title="Test"><span class="txt">Test</span></a>
          <div class="online_status">Online {status_text}</div>
        </li>
        """
        return BeautifulSoup(html, "lxml").select_one("li.resource_server_item")

    def test_real_count_is_kept(self):
        fetcher = PlanetMinecraftFetcher()
        server = fetcher._parse_item(self._item("3/40 players"))
        self.assertEqual(server.online_players, 3)
        self.assertEqual(server.max_players, 40)

    def test_sentinel_online_zeroes_both(self):
        fetcher = PlanetMinecraftFetcher()
        server = fetcher._parse_item(self._item("65,535/100 players"))
        self.assertEqual(server.online_players, 0)
        self.assertEqual(server.max_players, 0)

    def test_sentinel_max_zeroes_both(self):
        fetcher = PlanetMinecraftFetcher()
        server = fetcher._parse_item(self._item("10/65,535 players"))
        self.assertEqual(server.online_players, 0)
        self.assertEqual(server.max_players, 0)
