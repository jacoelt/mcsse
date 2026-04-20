from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from core.models import Server, Tag


def _make_server(name: str, ip: str, tag_names: list[str]) -> Server:
    server = Server.objects.create(name=name, ip_address=ip)
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(
            name=tag_name,
            defaults={"display_name": tag_name.title()},
        )
        server.tags.add(tag)
    return server


class ReconcileTagsCommandTest(TestCase):
    """End-to-end tests of the reconcile_tags management command."""

    def test_rename_in_place_when_no_collision(self):
        """Sole-source tag gets renamed, no M2M churn."""
        server = _make_server("S", "1.1.1.1", ["auctions"])
        original_id = Tag.objects.get(name="auctions").id

        call_command("reconcile_tags")

        self.assertFalse(Tag.objects.filter(name="auctions").exists())
        tag = Tag.objects.get(name="auction")
        self.assertEqual(tag.id, original_id)  # same row, renamed
        self.assertEqual(tag.display_name, "Auction")
        self.assertIn(tag, server.tags.all())

    def test_merge_into_existing_canonical(self):
        """Plural + singular exist; plural merges into singular."""
        server_a = _make_server("A", "1.1.1.1", ["clan"])
        server_b = _make_server("B", "2.2.2.2", ["clans"])

        call_command("reconcile_tags")

        self.assertFalse(Tag.objects.filter(name="clans").exists())
        target = Tag.objects.get(name="clan")
        self.assertIn(target, server_a.tags.all())
        self.assertIn(target, server_b.tags.all())

    def test_merge_dedups_existing_m2m(self):
        """If a server already has both source and target, no unique-constraint crash."""
        server = _make_server("S", "1.1.1.1", ["clan", "clans"])
        self.assertEqual(server.tags.count(), 2)

        call_command("reconcile_tags")

        self.assertEqual(server.tags.count(), 1)
        self.assertEqual(server.tags.first().name, "clan")

    def test_stopword_tag_is_deleted_and_server_unaffected(self):
        server = _make_server("S", "1.1.1.1", ["amazing", "survival"])

        call_command("reconcile_tags")

        self.assertFalse(Tag.objects.filter(name="amazing").exists())
        self.assertTrue(Server.objects.filter(id=server.id).exists())
        self.assertEqual(
            set(server.tags.values_list("name", flat=True)), {"survival"}
        )

    def test_bare_numeric_tag_is_deleted(self):
        _make_server("S", "1.1.1.1", ["1710", "survival"])

        call_command("reconcile_tags")

        self.assertFalse(Tag.objects.filter(name="1710").exists())
        self.assertTrue(Tag.objects.filter(name="survival").exists())

    def test_alias_rewrite(self):
        """Aliased tags merge into their canonical form."""
        _make_server("A", "1.1.1.1", ["bedw"])
        _make_server("B", "2.2.2.2", ["bedwars"])

        call_command("reconcile_tags")

        self.assertFalse(Tag.objects.filter(name="bedw").exists())
        bedwars = Tag.objects.get(name="bedwars")
        self.assertEqual(bedwars.servers.count(), 2)

    def test_separator_variants_merge(self):
        """bed-wars, bed_wars, bed wars (already slugified as bed-wars, bed_wars, bed-wars in SlugField) all collapse."""
        _make_server("A", "1.1.1.1", ["bed-wars"])
        _make_server("B", "2.2.2.2", ["bedwars"])

        call_command("reconcile_tags")

        self.assertEqual(Tag.objects.filter(name__in=["bed-wars", "bedwars"]).count(), 1)
        bedwars = Tag.objects.get(name="bedwars")
        self.assertEqual(bedwars.servers.count(), 2)

    def test_dry_run_makes_no_writes(self):
        _make_server("S", "1.1.1.1", ["amazing", "clans", "1710"])
        before = set(Tag.objects.values_list("name", flat=True))

        out = StringIO()
        call_command("reconcile_tags", "--dry-run", stdout=out)

        after = set(Tag.objects.values_list("name", flat=True))
        self.assertEqual(before, after)
        self.assertIn("dry-run", out.getvalue())

    def test_idempotent_on_clean_data(self):
        """Running against already-canonical data is a no-op."""
        _make_server("S", "1.1.1.1", ["survival", "pvp", "bedwars"])
        before = set(Tag.objects.values_list("name", flat=True))

        call_command("reconcile_tags")
        after = set(Tag.objects.values_list("name", flat=True))

        self.assertEqual(before, after)

    def test_multiple_sources_to_new_canonical_target(self):
        """3 non-canonical tags all mapping to a canonical that doesn't yet exist:
        one gets promoted (renamed), the other two merge into it."""
        server_a = _make_server("A", "1.1.1.1", ["bedw"])
        server_b = _make_server("B", "2.2.2.2", ["bedwar"])
        # Both bedw and bedwar alias to bedwars; bedwars doesn't exist yet.

        call_command("reconcile_tags")

        self.assertEqual(Tag.objects.filter(name__in=["bedw", "bedwar"]).count(), 0)
        bedwars = Tag.objects.get(name="bedwars")
        self.assertEqual(
            set(bedwars.servers.values_list("id", flat=True)),
            {server_a.id, server_b.id},
        )

    def test_verbose_output_lists_each_action(self):
        _make_server("S", "1.1.1.1", ["clans", "amazing", "bedw"])

        out = StringIO()
        call_command("reconcile_tags", "--dry-run", verbosity=2, stdout=out)
        text = out.getvalue()

        self.assertIn("clans", text)
        self.assertIn("amazing", text)
        self.assertIn("bedw", text)
