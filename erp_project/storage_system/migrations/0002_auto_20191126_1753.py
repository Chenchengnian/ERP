# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-11-26 09:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='顾客生日,格式:1999-01-01'),
        ),
    ]