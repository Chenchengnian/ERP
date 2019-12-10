# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-12-09 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_system', '0002_auto_20191209_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(choices=[('未入库', '未入库'), ('已入库', '已入库'), ('需补货', '需补货'), ('已出售', '已出售')], max_length=32, verbose_name='状态'),
        ),
    ]
