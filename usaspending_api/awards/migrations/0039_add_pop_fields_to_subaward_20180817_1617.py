# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-17 16:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("awards", "0038_auto_20180815_1832")]

    operations = [
        migrations.RenameField(model_name="subaward", old_name="pop_zip5", new_name="pop_zip4"),
        migrations.AddField(model_name="subaward", name="pop_city_name", field=models.TextField(blank=True, null=True)),
        migrations.AddField(
            model_name="subaward", name="pop_state_name", field=models.TextField(blank=True, null=True)
        ),
        migrations.AddField(
            model_name="subaward", name="pop_street_address", field=models.TextField(blank=True, null=True)
        ),
        migrations.AddField(
            model_name="subaward", name="recipient_location_city_code", field=models.TextField(blank=True, null=True)
        ),
        migrations.AddField(
            model_name="subaward", name="recipient_location_city_name", field=models.TextField(blank=True, null=True)
        ),
        migrations.AlterField(model_name="subaward", name="data_source", field=models.TextField(blank=True, null=True)),
    ]
