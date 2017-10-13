# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-02 02:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0051_auto_20170802_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='order_priority',
            field=models.ForeignKey(blank=True, default=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='cpm.OrderPriority'),
        ),
    ]