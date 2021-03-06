# Generated by Django 2.1.7 on 2019-02-23 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0008_media_source"),
    ]

    operations = [
        migrations.AddField(
            model_name="license",
            name="href",
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name="license",
            name="name",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="license",
            name="short_name",
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
