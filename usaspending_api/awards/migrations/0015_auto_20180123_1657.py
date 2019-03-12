# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-23 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("awards", "0014_merge_20180116_1511")]

    operations = [
        migrations.CreateModel(
            name="SummaryTransactionGeoView",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action_date", models.DateField()),
                ("fiscal_year", models.IntegerField()),
                ("type", models.TextField()),
                ("pulled_from", models.TextField()),
                ("recipient_location_country_name", models.TextField()),
                ("recipient_location_country_code", models.TextField()),
                ("recipient_location_state_code", models.TextField()),
                ("recipient_location_county_name", models.TextField()),
                ("recipient_location_county_code", models.TextField()),
                ("recipient_location_zip5", models.TextField()),
                ("recipient_location_congressional_code", models.TextField()),
                ("recipient_location_foreign_province", models.TextField()),
                ("pop_country_name", models.TextField()),
                ("pop_country_code", models.TextField()),
                ("pop_state_code", models.TextField()),
                ("pop_county_name", models.TextField()),
                ("pop_county_code", models.TextField()),
                ("pop_zip5", models.TextField()),
                ("pop_congressional_code", models.TextField()),
                ("awarding_agency_id", models.IntegerField()),
                ("funding_agency_id", models.IntegerField()),
                ("awarding_toptier_agency_name", models.TextField()),
                ("funding_toptier_agency_name", models.TextField()),
                ("awarding_subtier_agency_name", models.TextField()),
                ("funding_subtier_agency_name", models.TextField()),
                ("awarding_toptier_agency_abbreviation", models.TextField()),
                ("funding_toptier_agency_abbreviation", models.TextField()),
                ("awarding_subtier_agency_abbreviation", models.TextField()),
                ("funding_subtier_agency_abbreviation", models.TextField()),
                (
                    "federal_action_obligation",
                    models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
                ),
                ("counts", models.IntegerField()),
            ],
            options={"managed": False, "db_table": "summary_transaction_geo_view"},
        ),
        migrations.AddField(
            model_name="award",
            name="generated_unique_award_id",
            field=models.TextField(default="none", verbose_name="Generated Unique Award ID"),
        ),
        migrations.AddField(
            model_name="award", name="is_fpds", field=models.BooleanField(default=False, verbose_name="Is FPDS")
        ),
        migrations.AddField(
            model_name="award",
            name="parent_award_piid",
            field=models.TextField(
                help_text="The piid of the Award's parent Award", null=True, verbose_name="Parent Award Piid"
            ),
        ),
        migrations.AddField(
            model_name="award",
            name="transaction_unique_id",
            field=models.TextField(default="none", verbose_name="Transaction Unique ID"),
        ),
        migrations.AddField(
            model_name="transactionnormalized",
            name="transaction_unique_id",
            field=models.TextField(default="none", verbose_name="Transaction Unique ID"),
        ),
    ]
