# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-26 20:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("bulk_download", "0004_bulkdownloadjob_keyword")]

    operations = [
        migrations.RemoveField(model_name="bulkdownloadjob", name="agency"),
        migrations.RemoveField(model_name="bulkdownloadjob", name="job_status"),
        migrations.DeleteModel(name="BulkDownloadJob"),
    ]
