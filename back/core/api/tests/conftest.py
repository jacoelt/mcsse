import pytest

from core.models import Server, ServerTag


@pytest.fixture
def server_tag_factory(db, faker):

    def create_server_tag(**kwargs):
        defaults = {
            "name": faker.word(),
            "description": faker.text(),
            "relevance": faker.random_int(min=1, max=10),
        }
        defaults.update(kwargs)
        return ServerTag.objects.create(**defaults)

    return create_server_tag


@pytest.fixture
def server_factory(db, faker):

    def create_server(**kwargs):
        defaults = {
            "name": faker.name(),
            "description": faker.text(),
            "ip_address_java": faker.url(),
            "ip_address_bedrock": faker.url(),
            "versions": ",".join(
                faker.random_elements(
                    elements=[
                        "1.16",
                        "1.17",
                        "1.18",
                        "1.19",
                        "1.19.1",
                        "1.19.2",
                        "1.19.3",
                        "1.20",
                    ],
                    unique=True,
                    length=faker.random_int(min=1, max=5),
                )
            ),
            "players_online": faker.random_int(min=0, max=100),
            "max_players": faker.random_int(min=0, max=100),
            "banner": faker.image_url(),
            "added_at": faker.date_time_this_year(),
            "status": "online",
            "total_votes": faker.random_int(min=0, max=1000),
            "country": faker.country_code(),
            "languages": ",".join(
                faker.random_elements(
                    elements=["en", "fr", "de", "es", "ru"],
                    unique=True,
                    length=faker.random_int(min=1, max=3),
                )
            ),
            "website": faker.url(),
            "discord": faker.url(),
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
def tag_1(server_tag_factory):
    return server_tag_factory(name="tag1", description="Tag 1", relevance=0)


@pytest.fixture
def tag_list(server_tag_factory):
    return [
        server_tag_factory(name=f"tag{i}", description=f"Tag {i}", relevance=i)
        for i in range(1, 20)
    ]


@pytest.fixture
def server_1(db, server_factory, tag_1):
    return server_factory(
        name="Test Server 1",
        tags=[tag_1],
    )


@pytest.fixture
def server_with_java_url(db, server_factory):
    return server_factory(
        name="Test Server with Java url",
        ip_address_java="123.123.123.123:1234",
    )


@pytest.fixture
def server_list(db, server_factory, tag_list):
    return [
        server_factory(
            name=f"Test Server {i}",
            tags=tag_list[:i],
        )
        for i in range(1, 21)
    ]
