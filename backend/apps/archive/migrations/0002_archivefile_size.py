# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-05 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("archive", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="archivefile",
            name="size",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
