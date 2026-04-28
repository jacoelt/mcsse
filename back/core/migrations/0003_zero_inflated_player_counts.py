from django.db import migrations
from django.db.models import F, Q

# Mirror of fetcher.reconciler.MAX_PLAUSIBLE_PLAYERS. Duplicated here because
# migrations must be self-contained and not import application code that may
# change over time.
MAX_PLAUSIBLE_PLAYERS = 20_000


def zero_inflated_player_counts(apps, schema_editor):
    Server = apps.get_model("core", "Server")
    bad = Server.objects.filter(
        Q(online_players__gt=MAX_PLAUSIBLE_PLAYERS)
        | Q(max_players__gt=MAX_PLAUSIBLE_PLAYERS)
        | Q(max_players__gt=0, online_players__gt=F("max_players"))
    )
    bad.update(online_players=0, max_players=0, is_online=False)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_create_superuser"),
    ]

    operations = [
        migrations.RunPython(zero_inflated_player_counts, migrations.RunPython.noop),
    ]
