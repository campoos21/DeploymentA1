# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-19 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forkilla', '0003_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(),
        ),
    ]
