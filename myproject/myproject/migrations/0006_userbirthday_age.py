# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2020-03-16 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0005_userbirthday'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbirthday',
            name='age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]