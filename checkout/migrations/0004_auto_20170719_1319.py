# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20170717_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='comment',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
