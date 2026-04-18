import threading

from django.conf import settings
from django.core.management import call_command
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Query

from core.models import Server, Tag

from .schemas import (
    CountryCountSchema,
    FiltersResponseSchema,
    PaginatedResponseSchema,
    ServerDetailSchema,
    ServerFilterSchema,
    TagWithCountSchema,
    VersionCountSchema,
)

api = NinjaAPI(title="MC Server Search", version="1.0.0")

VALID_SORT_FIELDS = {
    "name",
    "-name",
    "online_players",
    "-online_players",
    "max_players",
    "-max_players",
    "votes",
    "-votes",
    "created_at",
    "-created_at",
    "game_version",
    "-game_version",
}


@api.get("/servers/", response=PaginatedResponseSchema)
def list_servers(
    request,
    filters: ServerFilterSchema = Query(...),
    tags: str = None,
    sort: str = "-online_players",
    page: int = 1,
    page_size: int = 20,
):
    qs = Server.objects.prefetch_related("tags").all()
    qs = filters.filter(qs)

    if tags:
        tag_slugs = [t.strip() for t in tags.split(",") if t.strip()]
        for slug in tag_slugs:
            qs = qs.filter(tags__name=slug)

    if sort in VALID_SORT_FIELDS:
        qs = qs.order_by(sort)

    page_size = min(max(page_size, 1), 100)
    page = max(page, 1)

    count = qs.count()
    offset = (page - 1) * page_size
    results = qs[offset : offset + page_size]

    return {
        "count": count,
        "page": page,
        "page_size": page_size,
        "results": results,
    }


@api.get("/servers/{server_id}/", response=ServerDetailSchema)
def get_server(request, server_id: str):
    server = get_object_or_404(
        Server.objects.prefetch_related("tags", "sources"),
        id=server_id,
    )
    return server


@api.get("/filters/", response=FiltersResponseSchema)
def get_filters(request):
    versions = (
        Server.objects.exclude(game_version="")
        .values("game_version")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    countries = (
        Server.objects.exclude(country="")
        .values("country")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    tags = Tag.objects.annotate(count=Count("servers")).filter(count__gt=0).order_by("-count")

    return {
        "versions": [{"version": v["game_version"], "count": v["count"]} for v in versions],
        "countries": [{"country": c["country"], "count": c["count"]} for c in countries],
        "tags": [{"name": t.name, "display_name": t.display_name, "count": t.count} for t in tags],
    }


@api.post("/internal/fetch/")
def trigger_fetch(request, mode: str = "full"):
    api_key = request.headers.get("X-Fetch-Key", "")
    if api_key != settings.FETCH_API_KEY:
        return api.create_response(request, {"error": "unauthorized"}, status=403)

    command = "fetch_servers" if mode == "full" else "update_players"
    thread = threading.Thread(target=call_command, args=(command,))
    thread.start()

    return {"status": "started", "mode": mode}
