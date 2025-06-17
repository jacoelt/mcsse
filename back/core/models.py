import uuid
from django.db import models


class ServerTag(models.Model):
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

    EDITION_CHOICES = [
        ("java", "Java Edition"),
        ("bedrock", "Bedrock Edition"),
        ("both", "Java + Bedrock"),
    ]

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    ip_address_java = models.URLField(blank=True, null=True)
    ip_address_bedrock = models.URLField(blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    players_online = models.PositiveIntegerField(default=0)
    max_players = models.PositiveIntegerField(default=0)
    motd = models.TextField(blank=True, null=True)
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
    edition = models.CharField(
        max_length=10,
        choices=EDITION_CHOICES,
        default="java",
    )
    website = models.URLField(blank=True, null=True)
    discord = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address_java or self.ip_address_bedrock})"
