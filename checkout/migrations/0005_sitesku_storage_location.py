# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20170719_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesku',
            name='storage_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]