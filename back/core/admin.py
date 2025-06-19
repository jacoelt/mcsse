from django.contrib import admin


from .models import Server, ServerTag


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "ip_address_java",
        "ip_address_bedrock",
        "versions",
        "players_online",
        "max_players",
        "status",
        "added_at",
    )
    search_fields = ("name", "ip_address_java", "ip_address_bedrock")
    list_filter = ("status", "versions")
    ordering = ("-added_at",)


@admin.register(ServerTag)
class ServerTagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "relevance")
    search_fields = ("name",)
    ordering = ("name", "relevance")
