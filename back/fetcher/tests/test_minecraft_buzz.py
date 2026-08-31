from bs4 import BeautifulSoup
from django.test import SimpleTestCase

from fetcher.sources.minecraft_buzz import MinecraftBuzzFetcher


class MinecraftBuzzRowIdTest(SimpleTestCase):
    """The listing moved the server id off the row's `id` attribute and onto
    `data-server-id`, and demoted the name heading from <h3> to <h2>. Reading
    only `id` made _parse_row return None for all 30 rows on every page, so the
    source silently contributed nothing."""

    def _row(self, *, id_attr: str = "", data_server_id: str = "", heading: str = "h2"):
        attrs = ""
        if id_attr:
            attrs += f' id="{id_attr}"'
        if data_server_id:
            attrs += f' data-server-id="{data_server_id}"'
        html = f"""
        <table><tr class="row server-row server-listing"{attrs}>
          <td class="col-1">1</td>
          <td class="col-4"><{heading}>LemonCloud</{heading}></td>
          <td class="col-12">
            <data class="ip-block" value="buzz.lemoncloud.org">buzz.lemoncloud.org</data>
            <img src="https://crisps.minecraft.buzz/favicons/3096.png?v=1"/>
          </td>
          <td class="col-4">
            <span class="badge"><i class="fa fa-wrench text-black-50"></i>Version 1.7 to 26.2</span>
            <span class="badge"><i class="fa fa-tag text-black-50"></i>Survival Server</span>
            <span class="badge"><i class="fa fa-gamepad text-black-50"></i>Cross Platform</span>
          </td>
          <td class="col-1">6050/6150</td>
          <td class="col-3"><data class="badge" value="Online">Online</data></td>
          <td class="col-12 text-black-50 text-break"><p>Welcome to LemonCloud.</p></td>
        </tr></table>
        """
        return BeautifulSoup(html, "lxml").select_one("tr.server-row.server-listing")

    def test_data_server_id_is_used(self):
        fetcher = MinecraftBuzzFetcher()
        server = fetcher._parse_row(self._row(data_server_id="3096"))
        self.assertIsNotNone(server)
        self.assertEqual(server.external_id, "3096")
        self.assertEqual(server.name, "LemonCloud")

    def test_legacy_id_attribute_still_accepted(self):
        fetcher = MinecraftBuzzFetcher()
        server = fetcher._parse_row(self._row(id_attr="3096", heading="h3"))
        self.assertIsNotNone(server)
        self.assertEqual(server.external_id, "3096")
        self.assertEqual(server.name, "LemonCloud")

    def test_row_with_neither_id_is_skipped(self):
        fetcher = MinecraftBuzzFetcher()
        self.assertIsNone(fetcher._parse_row(self._row()))

    def test_remaining_fields_survive(self):
        fetcher = MinecraftBuzzFetcher()
        server = fetcher._parse_row(self._row(data_server_id="3096"))
        self.assertEqual(server.ip_address, "buzz.lemoncloud.org")
        self.assertEqual(server.game_version, "1.7 to 26.2")
        self.assertEqual(server.edition, "both")
        self.assertEqual(server.tags, ["Survival"])
        self.assertEqual(server.online_players, 6050)
        self.assertEqual(server.max_players, 6150)
        self.assertTrue(server.is_online)
        self.assertEqual(server.description, "Welcome to LemonCloud.")
        self.assertEqual(server.banner_url, "https://crisps.minecraft.buzz/favicons/3096.png?v=1")
