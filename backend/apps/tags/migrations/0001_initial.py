# Generated by Django 2.2.4 on 2019-09-06 09:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [("hav_collections", "0003_collection_public")]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="ManagedTag",
            fields=[
                (
                    "tag_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tags.Tag",
                    ),
                ),
                (
                    "source",
                    models.CharField(
                        choices=[("iso639_3", "languages"), ("iso3166", "countries")],
                        db_index=True,
                        max_length=20,
                    ),
                ),
                ("source_ref", models.CharField(db_index=True, max_length=20)),
            ],
            options={"unique_together": {("source", "source_ref")}},
            bases=("tags.tag",),
        ),
        migrations.CreateModel(
            name="CollectionTag",
            fields=[
                (
                    "tag_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tags.Tag",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="hav_collections.Collection",
                    ),
                ),
            ],
            bases=("tags.tag",),
        ),
    ]
