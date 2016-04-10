# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpm', '0019_auto_20160317_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=500)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpm.Role')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpm.Project')),
            ],
        ),
    ]