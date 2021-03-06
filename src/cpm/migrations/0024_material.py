# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-27 21:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0023_auto_20160319_0152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_category', models.CharField(max_length=500)),
                ('order_sub_category', models.CharField(max_length=500)),
                ('order_item', models.CharField(max_length=500)),
                ('order_item_url', models.URLField(max_length=1000)),
                ('order_quantity', models.IntegerField(validators=[django.core.validators.MaxValueValidator(250), django.core.validators.MinValueValidator(0)])),
                ('order_unit_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpm.Project')),
            ],
        ),
    ]
