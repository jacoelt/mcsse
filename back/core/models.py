from django.db import models

class Server(models.Model):
    ip_address = models.GenericIPAddressField(primary_key=True)
    name = models.CharField(max_length=255)
    port = models.PositiveIntegerField(default=25565)
    version = models.CharField(max_length=50, blank=True, null=True)
    players_online = models.PositiveIntegerField(default=0)
    max_players = models.PositiveIntegerField(default=0)
    motd = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address}:{self.port})"