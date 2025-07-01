from datetime import datetime, timedelta, timezone
from django.db.models import Q
from ninja import NinjaAPI

from core.api.schema import SearchIn, ServerOut
from core.models import Server


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


@api.get("/valuesLists")
def get_values_lists(request, response=dict):
    """
    Get values lists for filtering.
    """
    values_list = {
        "TBD": ["TBD"],  # TODO
    }
    return values_list
