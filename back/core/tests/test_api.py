from django.test import TestCase, Client

from core.models import Server, Tag

from .factories import ServerFactory, ServerSourceFactory, TagFactory


class ServerListAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag_surv = TagFactory(name="survival", display_name="Survival")
        self.tag_pvp = TagFactory(name="pvp", display_name="PvP")

        self.s1 = ServerFactory(
            name="AlphaCraft",
            game_version="1.21",
            edition="java",
            online_players=200,
            max_players=500,
            votes=100,
            country="US",
            tags=[self.tag_surv],
        )
        self.s2 = ServerFactory(
            name="BetaWorld",
            game_version="1.20",
            edition="bedrock",
            online_players=50,
            max_players=100,
            votes=500,
            country="DE",
            tags=[self.tag_surv, self.tag_pvp],
        )
        self.s3 = ServerFactory(
            name="GammaSMP",
            game_version="1.21.4",
            edition="both",
            online_players=1000,
            max_players=5000,
            votes=2000,
            country="US",
            tags=[self.tag_pvp],
        )

    def test_list_returns_all(self):
        resp = self.client.get("/api/servers/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["results"]), 3)

    def test_default_sort_by_players_desc(self):
        resp = self.client.get("/api/servers/")
        data = resp.json()
        players = [r["online_players"] for r in data["results"]]
        self.assertEqual(players, [1000, 200, 50])

    def test_sort_by_votes(self):
        resp = self.client.get("/api/servers/", {"sort": "-votes"})
        data = resp.json()
        votes = [r["votes"] for r in data["results"]]
        self.assertEqual(votes, [2000, 500, 100])

    def test_filter_by_name(self):
        resp = self.client.get("/api/servers/", {"q": "Alpha"})
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["name"], "AlphaCraft")

    def test_filter_by_version_prefix(self):
        resp = self.client.get("/api/servers/", {"version": "1.21"})
        data = resp.json()
        self.assertEqual(data["count"], 2)
        names = {r["name"] for r in data["results"]}
        self.assertEqual(names, {"AlphaCraft", "GammaSMP"})

    def test_filter_by_edition(self):
        resp = self.client.get("/api/servers/", {"edition": "bedrock"})
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["name"], "BetaWorld")

    def test_filter_by_player_range(self):
        resp = self.client.get("/api/servers/", {"players_min": 100, "players_max": 1000})
        data = resp.json()
        self.assertEqual(data["count"], 2)
        names = {r["name"] for r in data["results"]}
        self.assertEqual(names, {"AlphaCraft", "GammaSMP"})

    def test_filter_by_votes_range(self):
        resp = self.client.get("/api/servers/", {"votes_min": 200})
        data = resp.json()
        self.assertEqual(data["count"], 2)

    def test_filter_by_country(self):
        resp = self.client.get("/api/servers/", {"country": "DE"})
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["name"], "BetaWorld")

    def test_filter_by_tag(self):
        resp = self.client.get("/api/servers/", {"tags": "pvp"})
        data = resp.json()
        self.assertEqual(data["count"], 2)
        names = {r["name"] for r in data["results"]}
        self.assertEqual(names, {"BetaWorld", "GammaSMP"})

    def test_filter_by_multiple_tags(self):
        resp = self.client.get("/api/servers/", {"tags": "pvp,survival"})
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["name"], "BetaWorld")

    def test_pagination(self):
        resp = self.client.get("/api/servers/", {"page_size": 2, "page": 1})
        data = resp.json()
        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["results"]), 2)
        self.assertEqual(data["page"], 1)
        self.assertEqual(data["page_size"], 2)

    def test_pagination_page_2(self):
        resp = self.client.get("/api/servers/", {"page_size": 2, "page": 2})
        data = resp.json()
        self.assertEqual(len(data["results"]), 1)

    def test_page_size_clamped(self):
        resp = self.client.get("/api/servers/", {"page_size": 999})
        data = resp.json()
        self.assertEqual(data["page_size"], 100)

    def test_invalid_sort_ignored(self):
        resp = self.client.get("/api/servers/", {"sort": "hacked_field"})
        data = resp.json()
        # Falls back to default ordering (model Meta: -online_players)
        self.assertEqual(data["results"][0]["name"], "GammaSMP")

    def test_combined_filters(self):
        resp = self.client.get("/api/servers/", {
            "country": "US",
            "players_min": 100,
            "tags": "pvp",
        })
        data = resp.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["name"], "GammaSMP")

    def test_result_shape(self):
        resp = self.client.get("/api/servers/")
        result = resp.json()["results"][0]
        expected_keys = {
            "id", "name", "game_version", "edition", "online_players",
            "max_players", "votes", "country", "tags", "banner_url", "is_online",
        }
        self.assertTrue(expected_keys.issubset(result.keys()))
        self.assertIsInstance(result["tags"], list)


class ServerDetailAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag = TagFactory(name="survival")
        self.server = ServerFactory(
            name="DetailCraft",
            description="A detailed server",
            website_url="https://example.com",
            tags=[self.tag],
        )
        self.source = ServerSourceFactory(
            server=self.server,
            source_name="minecraft-mp",
            source_url="https://minecraft-mp.com/server-s1",
        )

    def test_get_detail(self):
        resp = self.client.get(f"/api/servers/{self.server.id}/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["name"], "DetailCraft")
        self.assertEqual(data["description"], "A detailed server")
        self.assertEqual(data["website_url"], "https://example.com")

    def test_detail_includes_tags(self):
        resp = self.client.get(f"/api/servers/{self.server.id}/")
        data = resp.json()
        self.assertEqual(len(data["tags"]), 1)
        self.assertEqual(data["tags"][0]["name"], "survival")

    def test_detail_includes_sources(self):
        resp = self.client.get(f"/api/servers/{self.server.id}/")
        data = resp.json()
        self.assertEqual(len(data["sources"]), 1)
        self.assertEqual(data["sources"][0]["source_name"], "minecraft-mp")

    def test_detail_shape(self):
        resp = self.client.get(f"/api/servers/{self.server.id}/")
        data = resp.json()
        expected_keys = {
            "id", "name", "ip_address", "port", "description", "game_version",
            "edition", "online_players", "max_players", "votes", "country",
            "website_url", "discord_url", "banner_url", "is_online", "tags",
            "sources", "created_at", "updated_at", "last_checked",
        }
        self.assertTrue(expected_keys.issubset(data.keys()))

    def test_detail_not_found(self):
        resp = self.client.get("/api/servers/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(resp.status_code, 404)


class FiltersAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        tag1 = TagFactory(name="survival")
        tag2 = TagFactory(name="pvp")
        TagFactory(name="unused")  # no servers — should not appear

        ServerFactory(game_version="1.21", country="US", tags=[tag1])
        ServerFactory(game_version="1.21", country="US", tags=[tag1, tag2])
        ServerFactory(game_version="1.20", country="DE", tags=[tag2])

    def test_filters_endpoint(self):
        resp = self.client.get("/api/filters/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("versions", data)
        self.assertIn("countries", data)
        self.assertIn("tags", data)

    def test_versions_with_counts(self):
        resp = self.client.get("/api/filters/")
        versions = {v["version"]: v["count"] for v in resp.json()["versions"]}
        self.assertEqual(versions["1.21"], 2)
        self.assertEqual(versions["1.20"], 1)

    def test_countries_with_counts(self):
        resp = self.client.get("/api/filters/")
        countries = {c["country"]: c["count"] for c in resp.json()["countries"]}
        self.assertEqual(countries["US"], 2)
        self.assertEqual(countries["DE"], 1)

    def test_tags_exclude_unused(self):
        resp = self.client.get("/api/filters/")
        tag_names = {t["name"] for t in resp.json()["tags"]}
        self.assertIn("survival", tag_names)
        self.assertIn("pvp", tag_names)
        self.assertNotIn("unused", tag_names)

    def test_tags_with_counts(self):
        resp = self.client.get("/api/filters/")
        tags = {t["name"]: t["count"] for t in resp.json()["tags"]}
        self.assertEqual(tags["survival"], 2)
        self.assertEqual(tags["pvp"], 2)
