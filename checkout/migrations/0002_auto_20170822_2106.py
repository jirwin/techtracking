# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-23 04:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='team',
            new_name='members',
        ),
    ]
