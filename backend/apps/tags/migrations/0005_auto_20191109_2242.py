# Generated by Django 2.2.4 on 2019-11-09 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hav_collections", "0003_collection_public"),
        ("tags", "0004_auto_20191107_1115"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="tag", unique_together={("name", "collection")}
        )
    ]