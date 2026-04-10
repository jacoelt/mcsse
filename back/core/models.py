import uuid

from django.contrib.postgres.indexes import GinIndex
from django.db import models


class Tag(models.Model):
    name = models.SlugField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name


class Server(models.Model):
    class Edition(models.TextChoices):
        JAVA = "java", "Java"
        BEDROCK = "bedrock", "Bedrock"
        BOTH = "both", "Java & Bedrock"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.CharField(max_length=255, blank=True, default="")
    port = models.IntegerField(default=25565)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    game_version = models.CharField(max_length=50, blank=True, default="")
    edition = models.CharField(
        max_length=10, choices=Edition.choices, default=Edition.JAVA
    )
    online_players = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    country = models.CharField(max_length=2, blank=True, default="")
    website_url = models.URLField(max_length=500, blank=True, default="")
    discord_url = models.URLField(max_length=500, blank=True, default="")
    banner_url = models.URLField(max_length=500, blank=True, default="")
    is_online = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="servers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["ip_address", "port"], name="idx_server_ip_port"),
            models.Index(fields=["game_version"], name="idx_server_version"),
            models.Index(fields=["edition"], name="idx_server_edition"),
            models.Index(fields=["country"], name="idx_server_country"),
            models.Index(fields=["online_players"], name="idx_server_online"),
            models.Index(fields=["max_players"], name="idx_server_max"),
            models.Index(fields=["votes"], name="idx_server_votes"),
            models.Index(fields=["created_at"], name="idx_server_created"),
            GinIndex(
                name="idx_server_name_trgm",
                fields=["name"],
                opclasses=["gin_trgm_ops"],
            ),
        ]
        ordering = ["-online_players"]

    def __str__(self):
        return self.name


class ServerSource(models.Model):
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="sources"
    )
    source_name = models.CharField(max_length=50)
    source_url = models.URLField(max_length=500, blank=True, default="")
    external_id = models.CharField(max_length=255)
    raw_data = models.JSONField(default=dict)
    last_fetched = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_name", "external_id"],
                name="uq_source_external",
            )
        ]

    def __str__(self):
        return f"{self.source_name}:{self.external_id}"
