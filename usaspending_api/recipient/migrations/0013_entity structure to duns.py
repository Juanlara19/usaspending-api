# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-20 19:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("recipient", "0012_summaryawardrecipient")]

    operations = [
        migrations.AddField(model_name="duns", name="entity_structure", field=models.TextField(blank=True, null=True))
    ]
