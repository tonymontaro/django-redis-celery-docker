# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-03-16 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0002_letterdigit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letterdigit',
            name='argument',
        ),
        migrations.AddField(
            model_name='letterdigit',
            name='string',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
