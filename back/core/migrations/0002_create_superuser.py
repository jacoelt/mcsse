import os

from django.db import migrations


def create_superuser(apps, schema_editor):
    username = os.environ.get("SUPER_USER_USERNAME")
    password = os.environ.get("SUPER_USER_PASSWORD")

    if not username or not password:
        return

    User = apps.get_model("auth", "User")
    if User.objects.filter(username=username).exists():
        return

    from django.contrib.auth.hashers import make_password

    User.objects.create(
        username=username,
        password=make_password(password),
        is_superuser=True,
        is_staff=True,
        is_active=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_superuser, migrations.RunPython.noop),
    ]
