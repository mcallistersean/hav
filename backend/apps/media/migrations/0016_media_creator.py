# Generated by Django 2.2.4 on 2019-08-19 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_names(apps, schema_editor):
    MediaCreator = apps.get_model("media", "MediaCreator")
    for mc in MediaCreator.objects.all().iterator():
        if mc.display_name:
            mc.name = mc.display_name
        else:
            mc.name = f"{mc.first_name} {mc.last_name}".strip()
        mc.save()


class Migration(migrations.Migration):

    dependencies = [
        ("media", "0015_auto_20190808_2148"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="mediacreator",
            name="created_by",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                related_query_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="mediacreator",
            name="modified_by",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                related_query_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="mediacreator",
            name="name",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
        migrations.RunPython(code=migrate_names),
        migrations.RemoveField(
            model_name="mediacreator",
            name="display_name",
        ),
        migrations.RemoveField(
            model_name="mediacreator",
            name="email",
        ),
        migrations.RemoveField(
            model_name="mediacreator",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="mediacreator",
            name="last_name",
        ),
    ]
