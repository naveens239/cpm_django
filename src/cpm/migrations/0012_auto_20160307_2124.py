# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-07 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0011_auto_20160307_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='member_role',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='project_name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]