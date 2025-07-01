from datetime import datetime, timedelta, timezone
from django.db import models
from django.db.models import Q
from ninja import NinjaAPI

from core.api.schema import SearchIn, ServerOut, ValuesListsOut
from core.models import Server, ServerTag


api = NinjaAPI(auth=None, csrf=False)


@api.post("/servers", response=list[ServerOut])
def list_servers(request, data: SearchIn):
    """
    List servers based on search criteria.
    """
    search_params = data
    query = Q()

    if search_params.query:
        query &= (
            Q(name__icontains=search_params.query)
            | Q(ip_address_java__icontains=search_params.query)
            | Q(ip_address_bedrock__icontains=search_params.query)
        )

    if search_params.versions:
        subquery = Q()
        for version in search_params.versions:
            subquery |= Q(versions__regex=rf"\b{version}\b")

        query &= subquery

    if search_params.edition:
        if search_params.edition == "java":
            query &= Q(ip_address_java__isnull=False)
        elif search_params.edition == "bedrock":
            query &= Q(ip_address_bedrock__isnull=False)
        elif search_params.edition == "both":
            query &= Q(ip_address_java__isnull=False) & Q(
                ip_address_bedrock__isnull=False
            )

    if search_params.players_online_min is not None:
        query &= Q(players_online__gte=search_params.players_online_min)

    if search_params.players_online_max is not None:
        query &= Q(players_online__lte=search_params.players_online_max)

    if search_params.max_players_min is not None:
        query &= Q(max_players__gte=search_params.max_players_min)

    if search_params.max_players_max is not None:
        query &= Q(max_players__lte=search_params.max_players_max)

    if search_params.days_prior is not None and search_params.days_prior > 0:
        time_delta = timedelta(days=search_params.days_prior)
        query &= Q(added_at__gte=(datetime.now(timezone.utc) - time_delta))

    if search_params.statuses:
        subquery = Q()
        for status in search_params.statuses:
            subquery |= Q(status=status)
        query &= subquery

    if search_params.total_votes_min is not None:
        query &= Q(total_votes__gte=search_params.total_votes_min)

    if search_params.total_votes_max is not None:
        query &= Q(total_votes__lte=search_params.total_votes_max)

    if search_params.countries:
        subquery = Q()
        for country in search_params.countries:
            subquery |= Q(country__iexact=country)
        query &= subquery

    if search_params.languages:
        subquery = Q()
        for language in search_params.languages:
            subquery |= Q(languages__icontains=language)
        query &= subquery

    if search_params.tags:
        through_table = Server.tags.through

        for tag in search_params.tags:
            query &= Q(
                id__in=through_table.objects.filter(
                    servertag__name__iexact=tag
                ).values_list(
                    "server_id",
                    flat=True,
                )
            )

    servers = Server.objects.filter(query).distinct()

    # Sorting
    sort_by = search_params.sort_by or "name"
    sort_order = "" if search_params.sort_order == "asc" else "-"

    servers = servers.order_by(f"{sort_order}{sort_by}")

    # Pagination
    page = search_params.page or 1
    page_size = search_params.page_size or 10
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return servers[start_index:end_index]


@api.get("/values-lists", response=ValuesListsOut)
def get_values_lists(request):
    """
    Get values lists for filtering.
    """

    versions_set = set()
    for server in Server.objects.all():
        if server.versions:
            versions_set.update(
                {version.strip() for version in server.versions.split(",")}
            )

    def version_sort_key(version):
        try:
            # Sort by major, minor, patch
            parts = version.split(".")
            return tuple(int(part) for part in parts)
        except ValueError:
            # If conversion fails, return a tuple that sorts last
            return (999, 999, 999)

    versions = sorted(versions_set, key=version_sort_key)

    countries = {
        country
        for country in Server.objects.filter(country__isnull=False)
        .values_list("country", flat=True)
        .distinct()
    }
    countries = sorted(countries)

    languages_set = set()
    for server in Server.objects.all():
        if server.languages:
            languages_set.update(
                {language.strip() for language in server.languages.split(",")}
            )
    languages = sorted(languages_set)

    tags = [
        {
            "name": tag.name,
            "description": tag.description,
            "relevance": tag.relevance,
        }
        for tag in ServerTag.objects.all().distinct().order_by("relevance")
    ]

    values_list = {
        "versions": versions,
        "editions": [
            {"value": Server.EDITION_JAVA, "label": "Java"},
            {"value": Server.EDITION_BEDROCK, "label": "Bedrock"},
            {"value": Server.EDITION_BOTH, "label": "Java & Bedrock"},
        ],
        "countries": countries,
        "languages": languages,
        "tags": tags,
        "dates": [
            {"label": "Last 24 hours", "value": 1},
            {"label": "Last 7 days", "value": 7},
            {"label": "Last month", "value": 30},
            {"label": "Last 3 months", "value": 90},
            {"label": "Last 6 months", "value": 180},
            {"label": "Last year", "value": 365},
            {"label": "Last 5 years", "value": 1825},
            {"label": "All time", "value": -1},  # -1 for all time
        ],
        "statuses": [
            {"value": status, "label": label} for status, label in Server.STATUS_CHOICES
        ],
        "max_votes": Server.objects.aggregate(max_votes=models.Max("total_votes")).get(
            "max_votes",
            10000,
        ),
        "max_online_players": Server.objects.aggregate(
            max_online_players=models.Max("players_online")
        ).get(
            "max_online_players",
            1000,
        ),
        "max_max_players": Server.objects.aggregate(
            max_max_players=models.Max("max_players")
        ).get(
            "max_max_players",
            1000,
        ),
    }
    return values_list
