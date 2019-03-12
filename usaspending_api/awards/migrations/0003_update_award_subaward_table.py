# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-06 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("awards", "0002_auto_20171101_1314")]

    operations = [
        migrations.AddField(
            model_name="subaward",
            name="award_type",
            field=models.TextField(
                db_index=True,
                default="unknown",
                help_text="Whether the parent award is a procurement or a grant",
                verbose_name="Award Type",
            ),
        ),
        migrations.AddField(
            model_name="subaward",
            name="broker_award_id",
            field=models.IntegerField(
                db_index=True,
                default=0,
                help_text="The ID of the parent award in broker",
                verbose_name="FSRS Award ID in the broker",
            ),
        ),
        migrations.AddField(
            model_name="subaward",
            name="internal_id",
            field=models.TextField(
                db_index=True,
                default="",
                help_text="The internal of the parent award in broker from FSRS",
                verbose_name="Internal ID of the parent award",
            ),
        ),
        migrations.AlterUniqueTogether(name="subaward", unique_together=set([])),
        migrations.RemoveField(model_name="subaward", name="naics"),
        migrations.RemoveField(model_name="subaward", name="naics_description"),
        migrations.RemoveField(model_name="subaward", name="submission"),
    ]
