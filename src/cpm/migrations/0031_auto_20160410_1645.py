# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-10 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0030_auto_20160409_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialcomment',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpm.Schedule'),
        ),
    ]