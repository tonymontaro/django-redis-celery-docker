# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-03-16 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0003_auto_20200316_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letterdigit',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('started', 'started'), ('finished', 'finished'), ('failed', 'failed')], default='pending', max_length=20),
        ),
    ]
