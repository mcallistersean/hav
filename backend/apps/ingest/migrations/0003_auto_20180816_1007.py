# Generated by Django 2.1 on 2018-08-16 10:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0005_media_collection"),
        ("ingest", "0002_ingestqueue_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ingestqueue",
            name="ingestion_items",
        ),
        migrations.AddField(
            model_name="ingestqueue",
            name="created_media_entries",
            field=models.ManyToManyField(blank=True, editable=False, to="media.Media"),
        ),
        migrations.AddField(
            model_name="ingestqueue",
            name="ingestion_queue",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.URLField(max_length=100), default=list, size=None
            ),
        ),
        migrations.AlterField(
            model_name="ingestqueue",
            name="name",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
