# Generated by Django 2.1.7 on 2019-02-23 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0012_auto_20190223_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='original_media_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='media.MediaType'),
        ),
    ]