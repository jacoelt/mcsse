# Generated by Django 5.2.2 on 2025-07-02 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_create_superuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="server",
            name="added_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
