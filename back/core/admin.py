from django.contrib import admin


from .models import Server, ServerTag


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "name",
        "version",
        "players_online",
        "max_players",
        "status",
        "added_at",
    )
    search_fields = ("name", "ip_address")
    list_filter = ("status", "version")
    ordering = ("-added_at",)


@admin.register(ServerTag)
class ServerTagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "relevance")
    search_fields = ("name",)
    ordering = ("name", "relevance")
