# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-26 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forkilla', '0013_auto_20190526_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='featured_photo',
            field=models.ImageField(default='fotos/default.png', upload_to='forkilla/static/fotos/'),
        ),
    ]
