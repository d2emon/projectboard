# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shortname', models.CharField(unique=True, max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
