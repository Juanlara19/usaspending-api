# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-29 04:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("references", "0020_legalentity_parent_recipient_name")]

    operations = [
        migrations.AddField(
            model_name="legalentityofficers",
            name="duns",
            field=models.TextField(blank=True, db_index=True, default="", null=True, verbose_name="DUNS Number"),
        )
    ]
