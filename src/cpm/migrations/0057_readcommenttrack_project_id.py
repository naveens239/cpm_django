# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-02 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0056_auto_20170902_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='readcommenttrack',
            name='project_id',
            field=models.IntegerField(default='20'),
            preserve_default=False,
        ),
    ]
