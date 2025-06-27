from datetime import timezone
import datetime
import uuid
import dateutil
import dateutil.parser
from django.db import models, transaction


class EditionChoices:
    java = "java"
    bedrock = "bedrock"
    both = "both"


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

    @property
    def edition(self):
        if self.ip_address_java and self.ip_address_bedrock:
            return EditionChoices.both

        if self.ip_address_bedrock:
            return EditionChoices.bedrock

        if self.ip_address_java:
            return EditionChoices.java

        return "N/A"

    def __str__(self):
        return f"{self.name} ({self.ip_address_java or self.ip_address_bedrock})"

    def updateData(self, new_data: "FetchedServer") -> None:  # type: ignore
        """
        Update the server data with new data from a fetcher.
        """
        self.name = new_data.name
        self.description = new_data.description
        self.ip_address_java = new_data.ip_address_java
        self.ip_address_bedrock = new_data.ip_address_bedrock
        self.versions = ",".join(new_data.versions)
        self.players_online = new_data.players_online
        self.max_players = new_data.max_players
        self.banner = new_data.banner
        self.added_at = (
            dateutil.parser.parse(new_data.added_at).replace(tzinfo=timezone.utc)
            if new_data.added_at
            else datetime.datetime.now(timezone.utc)
        )
        self.status = new_data.status or self.STATUS_UNKNOWN
        self.total_votes += new_data.total_votes
        self.country = new_data.country
        self.languages = ",".join(new_data.languages)
        self.website = new_data.website
        self.discord = new_data.discord

        # Save the updated server instance
        self.save()

        with transaction.atomic():
            # Clear existing tags and add new ones
            self.tags.clear()
            for tag in new_data.tags:
                db_tag = ServerTag.objects.filter(name=tag.name).first()
                if db_tag:
                    self.tags.add(db_tag)
