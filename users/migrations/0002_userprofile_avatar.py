# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 23:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]