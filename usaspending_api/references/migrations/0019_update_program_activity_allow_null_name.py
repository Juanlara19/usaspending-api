# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-15 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("references", "0018_auto_20180706_0316")]

    operations = [
        migrations.AlterField(
            model_name="refprogramactivity", name="program_activity_name", field=models.TextField(blank=True, null=True)
        )
    ]
