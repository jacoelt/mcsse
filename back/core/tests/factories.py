import factory
from django.utils import timezone

from core.models import Server, ServerSource, Tag


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"tag-{n}")
    display_name = factory.LazyAttribute(lambda o: o.name.replace("-", " ").title())


class ServerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Server

    name = factory.Sequence(lambda n: f"Server {n}")
    ip_address = factory.Sequence(lambda n: f"192.168.1.{n % 255}")
    port = 25565
    game_version = "1.21"
    edition = Server.Edition.JAVA
    online_players = 50
    max_players = 100
    votes = 10
    country = "US"
    is_online = True
    description = "A test server"

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.tags.add(*extracted)


class ServerSourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServerSource

    server = factory.SubFactory(ServerFactory)
    source_name = "minecraft-mp"
    source_url = factory.LazyAttribute(
        lambda o: f"https://minecraft-mp.com/server-s{o.external_id}"
    )
    external_id = factory.Sequence(lambda n: str(10000 + n))
    raw_data = factory.LazyFunction(dict)
