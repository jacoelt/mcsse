import uuid
from django.db import models


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

    STATUS_CHOICES = [
        ("online", "Online"),
        ("offline", "Offline"),
        ("unknown", "Unknown"),
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
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unknown",
    )
    total_votes = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(ServerTag, related_name="servers", blank=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    languages = models.CharField(max_length=511, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    discord = models.URLField(blank=True, null=True)

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

    def updateData(self, new_data):
        """
        Update the server data with new data from a scraper.
        """
        self.name = new_data.name
        self.ip_address_java = new_data.ip_address_java
        self.ip_address_bedrock = new_data.ip_address_bedrock
        self.versions = new_data.versions
        self.players_online = new_data.players_online
        self.max_players = new_data.max_players
        self.description = new_data.description
        self.banner = new_data.banner
        self.status = new_data.status
        self.total_votes += new_data.total_votes
        self.country = new_data.country
        self.languages = new_data.languages
        self.website = new_data.website
        self.discord = new_data.discord

        # Save the updated server instance
        self.save()

        self.tags.clear()
        for tag in new_data.tags.all():
            self.tags.add(tag)
