# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-02 02:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0050_material_order_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='order_priority',
            field=models.ForeignKey(default=100, on_delete=django.db.models.deletion.CASCADE, to='cpm.OrderPriority'),
        ),
    ]
