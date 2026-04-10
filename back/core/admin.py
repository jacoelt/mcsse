from django.contrib import admin

from core.models import Server, ServerSource, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "display_name"]
    search_fields = ["name", "display_name"]


class ServerSourceInline(admin.TabularInline):
    model = ServerSource
    extra = 0
    readonly_fields = ["source_name", "source_url", "external_id", "last_fetched"]


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = [
        "name", "ip_address", "port", "edition", "game_version",
        "online_players", "max_players", "votes", "country", "is_online",
    ]
    list_filter = ["edition", "is_online", "country"]
    search_fields = ["name", "ip_address"]
    readonly_fields = ["id", "created_at", "updated_at", "last_checked"]
    filter_horizontal = ["tags"]
    inlines = [ServerSourceInline]


@admin.register(ServerSource)
class ServerSourceAdmin(admin.ModelAdmin):
    list_display = ["server", "source_name", "external_id", "last_fetched"]
    list_filter = ["source_name"]
    search_fields = ["external_id", "server__name"]
