# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-12 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0041_auto_20170112_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='toptieragency',
            name='fpds_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]