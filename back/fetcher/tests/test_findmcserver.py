from django.test import SimpleTestCase

from fetcher.sources.findmcserver import FindMCServerFetcher


class FindMCServerParseCountryTest(SimpleTestCase):
    """_parse_item must only emit ISO 3166-1 alpha-2 codes for country.

    The findmcserver API returns full location names in serverLocation[].name
    (e.g. "United States"). Those would overflow Server.country's varchar(2)
    column and crash reconciliation. Regression test for issue #10.
    """

    def _item(self, server_location):
        return {
            "id": "abc",
            "slug": "abc-slug",
            "name": "TestServer",
            "javaAddress": "1.2.3.4",
            "javaPort": 25565,
            "serverLocation": server_location,
        }

    def test_full_country_name_is_dropped(self):
        fetcher = FindMCServerFetcher()
        server = fetcher._parse_item(self._item([{"name": "United States"}]))
        self.assertEqual(server.country, "")

    def test_empty_location_list_yields_empty_country(self):
        fetcher = FindMCServerFetcher()
        server = fetcher._parse_item(self._item([]))
        self.assertEqual(server.country, "")

    def test_two_letter_code_is_kept_uppercased(self):
        fetcher = FindMCServerFetcher()
        server = fetcher._parse_item(self._item([{"name": "us"}]))
        self.assertEqual(server.country, "US")

    def test_non_alpha_two_char_is_dropped(self):
        fetcher = FindMCServerFetcher()
        server = fetcher._parse_item(self._item([{"name": "12"}]))
        self.assertEqual(server.country, "")
