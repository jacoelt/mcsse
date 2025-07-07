from datetime import timezone
import datetime
import uuid
import dateutil
import dateutil.parser
from django.db import models, transaction

from fetcher.fetched_server import FetchedServer


class ServerTag(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    relevance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Server(models.Model):

    STATUS_ONLINE = "online"
    STATUS_OFFLINE = "offline"
    STATUS_UNKNOWN = "unknown"

    STATUS_CHOICES = [
        (STATUS_ONLINE, "Online"),
        (STATUS_OFFLINE, "Offline"),
        (STATUS_UNKNOWN, "Unknown"),
    ]

    EDITION_JAVA = "java"
    EDITION_BEDROCK = "bedrock"
    EDITION_BOTH = "both"

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ip_address_java = models.URLField(blank=True, null=True)
    ip_address_bedrock = models.URLField(blank=True, null=True)
    versions = models.CharField(max_length=511, blank=True, null=True)
    players_online = models.PositiveIntegerField(default=0)
    max_players = models.PositiveIntegerField(default=0)
    banner = models.URLField(blank=True, null=True)
    added_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unknown",
    )
    total_votes = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=2, blank=True, null=True)
    languages = models.CharField(max_length=511, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    discord = models.URLField(blank=True, null=True)

    tags = models.ManyToManyField(ServerTag, related_name="servers", blank=True)

    list_of_updated_fields = [
        "name",
        "description",
        "ip_address_java",
        "ip_address_bedrock",
        "versions",
        "players_online",
        "max_players",
        "banner",
        "added_at",
        "status",
        "total_votes",
        "country",
        "languages",
        "website",
        "discord",
    ]

    @property
    def edition(self):
        if self.ip_address_java and self.ip_address_bedrock:
            return self.EDITION_BOTH

        if self.ip_address_bedrock:
            return self.EDITION_BEDROCK

        if self.ip_address_java:
            return self.EDITION_JAVA

        return "N/A"

    def __str__(self):
        return f"{self.name} ({self.ip_address_java or self.ip_address_bedrock})"

    @classmethod
    def from_fetched_server(cls, fetched_server: FetchedServer) -> "Server":
        """
        Create a Server instance from a fetched server data.
        """
        server_instance = cls()
        server_instance.updateData(fetched_server)
        return server_instance

    def updateData(self, new_data: FetchedServer) -> None:
        """
        Update the server data with new data from a fetcher.
        """
        if new_data.name is not None and new_data.name.strip() != "":
            self.name = new_data.name.strip()
        if new_data.description is not None and new_data.description.strip() != "":
            self.description = new_data.description.strip()
        if (
            new_data.ip_address_java is not None
            and new_data.ip_address_java.strip() != ""
        ):
            self.ip_address_java = new_data.ip_address_java.strip()
        if (
            new_data.ip_address_bedrock is not None
            and new_data.ip_address_bedrock.strip() != ""
        ):
            self.ip_address_bedrock = new_data.ip_address_bedrock.strip()
        if new_data.versions:
            # Ensure versions is a list of unique versions
            new_data.versions = list(set(new_data.versions))
            self.versions = ",".join(new_data.versions)
        if new_data.players_online is not None:
            self.players_online = new_data.players_online
        if new_data.max_players is not None:
            self.max_players = new_data.max_players
        if new_data.banner is not None and new_data.banner.strip() != "":
            self.banner = new_data.banner.strip()
        if new_data.added_at is not None and new_data.added_at.strip() != "":
            self.added_at = (
                dateutil.parser.parse(new_data.added_at).replace(tzinfo=timezone.utc)
                if new_data.added_at
                else datetime.datetime.now(timezone.utc)
            )
        if new_data.status is not None:
            self.status = new_data.status
        if new_data.total_votes is not None:
            self.total_votes += new_data.total_votes
        if new_data.country is not None and new_data.country.strip() != "":
            self.country = new_data.country.strip()
        if new_data.languages is not None and new_data.languages:
            # Ensure languages is a list of unique languages
            new_data.languages = list(
                {lang.strip() for lang in new_data.languages if lang.strip()}
            )
            self.languages = ",".join(new_data.languages)
        if new_data.website is not None and new_data.website.strip() != "":
            self.website = new_data.website.strip()
        if new_data.discord is not None and new_data.discord.strip() != "":
            self.discord = new_data.discord.strip()

    def update_tags(self, new_data: FetchedServer) -> None:

        with transaction.atomic():
            # Clear existing tags and add new ones
            self.tags.clear()
            for tag in new_data.tags:
                db_tag = ServerTag.objects.filter(name=tag.name).first()
                if db_tag:
                    self.tags.add(db_tag)
