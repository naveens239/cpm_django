# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0024_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='order_status',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]