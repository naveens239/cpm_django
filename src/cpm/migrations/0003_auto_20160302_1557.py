# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0002_createnewproject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createnewproject',
            name='project_name',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
