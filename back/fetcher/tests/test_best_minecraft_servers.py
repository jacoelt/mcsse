from bs4 import BeautifulSoup
from django.test import SimpleTestCase

from fetcher.sources.best_minecraft_servers import BestMinecraftServersFetcher


class BestMinecraftServersHrefTest(SimpleTestCase):
    """The site switched from relative to absolute hrefs, which made the old
    `a[href^="/server-"]` prefix selector reject every row on the page — the
    fetcher returned zero servers while still finding 36 table rows. Match on
    the path fragment instead, and build source_url with urljoin so an absolute
    href isn't concatenated onto base_url."""

    def _row(self, href: str):
        html = f"""
        <table class="ui very basic table servers"><tr class="o">
          <td class="rank">1</td>
          <td class="name">
            <div class="server-td-name"><h3 class="server-name">
              <a href="{href}">Complex Gaming</a>
            </h3></div>
          </td>
          <td class="server">
            <button data-clipboard-text="bmc.mc-complex.com" data-port="25565">Copy IP</button>
            <p class="description">A wide range of gamemodes.</p>
          </td>
          <td class="players">8777/10000</td>
          <td class="status">bmc.mc-complex.com</td>
        </tr></table>
        """
        return BeautifulSoup(html, "lxml").select_one("table.servers tr.o")

    def test_absolute_href_is_parsed(self):
        fetcher = BestMinecraftServersFetcher()
        row = self._row("https://best-minecraft-servers.co/server-complex-gaming.2763")
        server = fetcher._parse_row(row)
        self.assertIsNotNone(server)
        self.assertEqual(server.external_id, "2763")
        self.assertEqual(server.name, "Complex Gaming")
        self.assertEqual(
            server.source_url,
            "https://best-minecraft-servers.co/server-complex-gaming.2763",
        )

    def test_relative_href_still_parsed(self):
        fetcher = BestMinecraftServersFetcher()
        server = fetcher._parse_row(self._row("/server-complex-gaming.2763"))
        self.assertIsNotNone(server)
        self.assertEqual(server.external_id, "2763")
        self.assertEqual(
            server.source_url,
            "https://best-minecraft-servers.co/server-complex-gaming.2763",
        )

    def test_remaining_fields_survive(self):
        fetcher = BestMinecraftServersFetcher()
        server = fetcher._parse_row(
            self._row("https://best-minecraft-servers.co/server-complex-gaming.2763")
        )
        self.assertEqual(server.ip_address, "bmc.mc-complex.com")
        self.assertEqual(server.port, 25565)
        self.assertEqual(server.description, "A wide range of gamemodes.")
        self.assertEqual(server.online_players, 8777)
        self.assertEqual(server.max_players, 10000)
        self.assertTrue(server.is_online)

    def test_row_without_server_link_is_skipped(self):
        fetcher = BestMinecraftServersFetcher()
        self.assertIsNone(fetcher._parse_row(self._row("/category/survival")))
