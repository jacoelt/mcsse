from django.test import TestCase

from core.models import Server, ServerSource, Tag
from fetcher.base import FetchedServer, PlayerCount
from fetcher.reconciler import reconcile_servers, update_player_counts


class ReconcilerDeduplicationTest(TestCase):
    """Test that servers from multiple sources are correctly deduplicated."""

    def test_dedup_by_ip_port(self):
        """Two sources with same IP:port produce one server."""
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="ServerA", ip_address="1.2.3.4", port=25565,
                online_players=100, max_players=200,
            )),
            ("topg", FetchedServer(
                external_id="99", name="ServerA", ip_address="1.2.3.4", port=25565,
                online_players=90, max_players=200,
            )),
        ]
        created, updated = reconcile_servers(fetched)
        self.assertEqual(created, 1)
        self.assertEqual(updated, 0)
        self.assertEqual(Server.objects.count(), 1)

    def test_dedup_by_name_fallback(self):
        """Servers without IP are deduped by name."""
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="MyCraft",
            )),
            ("topg", FetchedServer(
                external_id="2", name="MyCraft",
            )),
        ]
        created, updated = reconcile_servers(fetched)
        self.assertEqual(created, 1)
        self.assertEqual(Server.objects.count(), 1)

    def test_different_ips_create_separate_servers(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="ServerA", ip_address="1.1.1.1",
            )),
            ("minecraft-mp", FetchedServer(
                external_id="2", name="ServerB", ip_address="2.2.2.2",
            )),
        ]
        created, _ = reconcile_servers(fetched)
        self.assertEqual(created, 2)
        self.assertEqual(Server.objects.count(), 2)

    def test_existing_server_is_updated(self):
        """Re-running reconcile on an existing server updates it."""
        fetched1 = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="OldName", ip_address="5.5.5.5",
                online_players=10,
            )),
        ]
        reconcile_servers(fetched1)
        self.assertEqual(Server.objects.count(), 1)

        fetched2 = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="NewName", ip_address="5.5.5.5",
                online_players=50,
            )),
        ]
        created, updated = reconcile_servers(fetched2)
        self.assertEqual(created, 0)
        self.assertEqual(updated, 1)
        server = Server.objects.first()
        self.assertEqual(server.name, "NewName")
        self.assertEqual(server.online_players, 50)


class ReconcilerMergeRulesTest(TestCase):
    """Test field-level merge logic when combining multiple sources."""

    def test_priority_fields_use_highest_priority_source(self):
        """minecraft-mp (priority 1) values win over topg (priority 7)."""
        fetched = [
            ("topg", FetchedServer(
                external_id="t1", name="TopGName", ip_address="1.2.3.4",
                game_version="1.19", country="DE",
            )),
            ("minecraft-mp", FetchedServer(
                external_id="m1", name="MPName", ip_address="1.2.3.4",
                game_version="1.21", country="US",
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        self.assertEqual(server.name, "MPName")
        self.assertEqual(server.game_version, "1.21")
        self.assertEqual(server.country, "US")

    def test_votes_are_summed(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="VoteServer", ip_address="1.2.3.4",
                votes=100,
            )),
            ("topg", FetchedServer(
                external_id="2", name="VoteServer", ip_address="1.2.3.4",
                votes=50,
            )),
            ("minecraft-buzz", FetchedServer(
                external_id="3", name="VoteServer", ip_address="1.2.3.4",
                votes=25,
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        self.assertEqual(server.votes, 175)

    def test_description_uses_longest(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="DescServer", ip_address="1.2.3.4",
                description="Short",
            )),
            ("topg", FetchedServer(
                external_id="2", name="DescServer", ip_address="1.2.3.4",
                description="This is a much longer description for the server",
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        self.assertEqual(server.description, "This is a much longer description for the server")

    def test_tags_are_unioned(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="TagServer", ip_address="1.2.3.4",
                tags=["Survival", "PvP"],
            )),
            ("topg", FetchedServer(
                external_id="2", name="TagServer", ip_address="1.2.3.4",
                tags=["PvP", "Skyblock"],
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        tag_names = set(server.tags.values_list("name", flat=True))
        self.assertEqual(tag_names, {"survival", "pvp", "skyblock"})

    def test_empty_field_falls_through_to_lower_priority(self):
        """If highest-priority source has empty field, use next source."""
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="FallThrough", ip_address="1.2.3.4",
                country="",  # empty
            )),
            ("topg", FetchedServer(
                external_id="2", name="FallThrough", ip_address="1.2.3.4",
                country="FR",
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        self.assertEqual(server.country, "FR")

    def test_players_uses_highest_value(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="1", name="PlayerServer", ip_address="1.2.3.4",
                online_players=50, max_players=100,
            )),
            ("topg", FetchedServer(
                external_id="2", name="PlayerServer", ip_address="1.2.3.4",
                online_players=200, max_players=500,
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        self.assertEqual(server.online_players, 200)
        self.assertEqual(server.max_players, 500)


class ReconcilerSourceTrackingTest(TestCase):
    """Test that ServerSource records are created and updated."""

    def test_sources_created_for_each_fetcher(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="m1", name="MultiSource", ip_address="1.2.3.4",
            )),
            ("topg", FetchedServer(
                external_id="t1", name="MultiSource", ip_address="1.2.3.4",
            )),
        ]
        reconcile_servers(fetched)
        self.assertEqual(ServerSource.objects.count(), 2)
        sources = set(ServerSource.objects.values_list("source_name", flat=True))
        self.assertEqual(sources, {"minecraft-mp", "topg"})

    def test_sources_linked_to_correct_server(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="m1", name="LinkedServer", ip_address="1.2.3.4",
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        source = ServerSource.objects.first()
        self.assertEqual(source.server_id, server.id)

    def test_source_updated_on_refetch(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="m1", name="Refetch", ip_address="1.2.3.4",
                source_url="https://example.com/v1",
            )),
        ]
        reconcile_servers(fetched)

        fetched[0] = ("minecraft-mp", FetchedServer(
            external_id="m1", name="Refetch", ip_address="1.2.3.4",
            source_url="https://example.com/v2",
        ))
        reconcile_servers(fetched)

        self.assertEqual(ServerSource.objects.count(), 1)
        self.assertEqual(ServerSource.objects.first().source_url, "https://example.com/v2")


class UpdatePlayerCountsTest(TestCase):
    """Test the hourly player count update path."""

    def test_update_existing_server(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="m1", name="CountServer", ip_address="1.2.3.4",
                online_players=10, is_online=True,
            )),
        ]
        reconcile_servers(fetched)
        server = Server.objects.first()
        self.assertEqual(server.online_players, 10)

        counts = [
            ("minecraft-mp", PlayerCount(
                external_id="m1", online_players=999, is_online=True,
            )),
        ]
        updated = update_player_counts(counts)
        self.assertEqual(updated, 1)
        server.refresh_from_db()
        self.assertEqual(server.online_players, 999)

    def test_update_skips_unknown_source(self):
        counts = [
            ("minecraft-mp", PlayerCount(
                external_id="nonexistent", online_players=50, is_online=True,
            )),
        ]
        updated = update_player_counts(counts)
        self.assertEqual(updated, 0)

    def test_update_sets_offline(self):
        fetched = [
            ("minecraft-mp", FetchedServer(
                external_id="m1", name="OfflineTest", ip_address="1.2.3.4",
                online_players=100, is_online=True,
            )),
        ]
        reconcile_servers(fetched)

        counts = [
            ("minecraft-mp", PlayerCount(
                external_id="m1", online_players=0, is_online=False,
            )),
        ]
        update_player_counts(counts)
        server = Server.objects.first()
        self.assertFalse(server.is_online)
        self.assertEqual(server.online_players, 0)
