from datetime import datetime, timedelta, timezone
import pytest

from core.models import Server, ServerTag


LIST_SERVER_COUNT = 20


@pytest.fixture
def server_tag_factory(db):

    def create_server_tag(**kwargs):
        defaults = {
            "name": "Test Tag",
            "description": "Test Tag Description",
            "relevance": 0,
        }
        defaults.update(kwargs)
        return ServerTag.objects.create(**defaults)

    return create_server_tag


@pytest.fixture
def server_factory(db):

    def create_server(**kwargs):
        defaults = {
            "name": "Test Server",
            "description": "",
            "ip_address_java": "http://example-java.com",
            "ip_address_bedrock": "http://example-bedrock.com",
            "versions": "1.16,1.17,1.18,1.19,1.19.1,1.19.2,1.19.3,1.20",
            "players_online": 42,
            "max_players": 100,
            "banner": "http://example.com/banner.png",
            "added_at": datetime.now(timezone.utc) - timedelta(days=30),
            "status": "online",
            "total_votes": 666,
            "country": "us",
            "languages": "en,fr",
            "website": "http://example-website.com",
            "discord": "http://example-discord.com",
        }
        defaults.update(kwargs)

        try:
            tags = defaults.pop("tags")
            server = Server.objects.create(**defaults)
            server.tags.set(tags)
        except KeyError:
            server = Server.objects.create(**defaults)

        return server

    return create_server


@pytest.fixture
def tag_list(server_tag_factory):
    return [
        server_tag_factory(name=f"tag{i}", description=f"Tag {i}", relevance=i)
        for i in range(1, 20)
    ]


@pytest.fixture
def server_list(db, server_factory):
    return [
        server_factory(
            name=f"Test Server {i}",
            ip_address_java=f"0.0.0.{i+1}:25565",
            ip_address_bedrock=f"0.0.0.{i+2}:19132",
        )
        for i in range(1, LIST_SERVER_COUNT + 1)
    ]


@pytest.fixture
def simple_server(db, server_factory, tag_list):
    return server_factory()


@pytest.fixture
def server_with_version_121(db, server_factory):
    return server_factory(
        name="Test Server with Version 1.21",
        versions="1.21",
    )


@pytest.fixture
def server_with_version_1211(db, server_factory):
    return server_factory(
        name="Test Server with Version 1.21.1",
        versions="1.21.1",
    )


@pytest.fixture
def server_with_no_java_ip(db, server_factory):
    return server_factory(
        name="Test Server with No Java IP",
        ip_address_java=None,
    )


@pytest.fixture
def server_with_no_bedrock_ip(db, server_factory):
    return server_factory(
        name="Test Server with No Bedrock IP",
        ip_address_bedrock=None,
    )


@pytest.fixture
def server_with_high_players_online(db, server_factory):
    return server_factory(
        name="Test Server with High Players Online",
        players_online=99,
    )


@pytest.fixture
def server_with_low_players_online(db, server_factory):
    return server_factory(
        name="Test Server with Low Players Online",
        players_online=1,
    )


@pytest.fixture
def server_with_high_max_players(db, server_factory):
    return server_factory(
        name="Test Server with High Max Players",
        max_players=200,
    )


@pytest.fixture
def server_with_low_max_players(db, server_factory):
    return server_factory(
        name="Test Server with Low Max Players",
        max_players=1,
    )


@pytest.fixture
def server_added_recently(db, server_factory):
    return server_factory(
        name="Test Server Added Recently",
        added_at=datetime.now(timezone.utc) - timedelta(days=1),
    )


@pytest.fixture
def server_added_long_ago(db, server_factory):
    return server_factory(
        name="Test Server Added Long Ago",
        added_at=datetime.now(timezone.utc) - timedelta(days=365),
    )


@pytest.fixture
def server_with_status_offline(db, server_factory):
    return server_factory(
        name="Test Server with Status Offline",
        status="offline",
    )


@pytest.fixture
def server_with_status_unknown(db, server_factory):
    return server_factory(
        name="Test Server with Status Unknown",
        status="unknown",
    )


@pytest.fixture
def server_with_high_total_votes(db, server_factory):
    return server_factory(
        name="Test Server with High Total Votes",
        total_votes=1000,
    )


@pytest.fixture
def server_with_low_total_votes(db, server_factory):
    return server_factory(
        name="Test Server with Low Total Votes",
        total_votes=1,
    )


@pytest.fixture
def server_with_country_ca(db, server_factory):
    return server_factory(
        name="Test Server with Country CA",
        country="ca",
    )


@pytest.fixture
def server_with_language_es(db, server_factory):
    return server_factory(
        name="Test Server with Language ES",
        languages="es",
    )


@pytest.fixture
def server_with_3tags(db, server_factory, tag_list):
    return server_factory(
        name="Test Server with 3 Tags",
        tags=[tag_list[0], tag_list[1], tag_list[2]],
    )


@pytest.fixture
def server_with_5tags(db, server_factory, tag_list):
    return server_factory(
        name="Test Server with 5 Tags",
        tags=[tag_list[0], tag_list[1], tag_list[2], tag_list[3], tag_list[4]],
    )
