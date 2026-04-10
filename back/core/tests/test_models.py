from django.test import TestCase

from core.models import Server, ServerSource, Tag

from .factories import ServerFactory, ServerSourceFactory, TagFactory


class TagModelTest(TestCase):
    def test_create_tag(self):
        tag = TagFactory(name="survival", display_name="Survival")
        self.assertEqual(str(tag), "Survival")
        self.assertEqual(tag.name, "survival")

    def test_unique_slug(self):
        Tag.objects.create(name="pvp", display_name="PvP")
        with self.assertRaises(Exception):
            Tag.objects.create(name="pvp", display_name="PvP")


class ServerModelTest(TestCase):
    def test_create_server(self):
        server = ServerFactory(name="TestCraft")
        self.assertEqual(str(server), "TestCraft")
        self.assertIsNotNone(server.id)
        self.assertTrue(server.created_at)

    def test_default_ordering(self):
        s1 = ServerFactory(online_players=10)
        s2 = ServerFactory(online_players=100)
        s3 = ServerFactory(online_players=50)
        servers = list(Server.objects.all())
        self.assertEqual(servers, [s2, s3, s1])

    def test_tags_relationship(self):
        tag1 = TagFactory(name="survival")
        tag2 = TagFactory(name="pvp")
        server = ServerFactory(tags=[tag1, tag2])
        self.assertEqual(server.tags.count(), 2)
        self.assertIn(tag1, server.tags.all())

    def test_edition_choices(self):
        for edition in ["java", "bedrock", "both"]:
            server = ServerFactory(edition=edition)
            self.assertEqual(server.edition, edition)


class ServerSourceModelTest(TestCase):
    def test_create_source(self):
        source = ServerSourceFactory(source_name="topg", external_id="12345")
        self.assertEqual(str(source), "topg:12345")

    def test_unique_constraint(self):
        ServerSourceFactory(source_name="minecraft-mp", external_id="99999")
        with self.assertRaises(Exception):
            ServerSourceFactory(source_name="minecraft-mp", external_id="99999")

    def test_cascade_delete(self):
        source = ServerSourceFactory()
        server = source.server
        server.delete()
        self.assertEqual(ServerSource.objects.filter(id=source.id).count(), 0)
