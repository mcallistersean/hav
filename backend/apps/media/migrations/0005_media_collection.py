# Generated by Django 2.0.6 on 2018-07-07 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("hav_collections", "0002_collection_root_node"),
        ("media", "0004_auto_20180205_1428"),
    ]

    operations = [
        migrations.AddField(
            model_name="media",
            name="collection",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="hav_collections.Collection",
            ),
        ),
    ]
