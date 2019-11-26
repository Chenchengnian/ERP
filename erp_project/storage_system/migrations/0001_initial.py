# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-11-26 09:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='分类')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否可见')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类信息',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='media/custom/default.png', upload_to='media/custom', verbose_name='顾客照片')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='顾客姓名')),
                ('cellphone', models.CharField(max_length=200, verbose_name='顾客电话')),
                ('wechat', models.CharField(max_length=200, verbose_name='顾客微信')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='顾客生日')),
                ('address', models.CharField(max_length=200, verbose_name='顾客地址')),
                ('user_info', models.TextField(blank=True, null=True, verbose_name='顾客信息')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否可见')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '顾客',
                'verbose_name_plural': '顾客信息',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='商品名称')),
                ('price', models.FloatField(verbose_name='商品价格')),
                ('image', models.ImageField(default='media/product/default.png', upload_to='media/product', verbose_name='商品图片')),
                ('sale_date', models.DateTimeField(blank=True, null=True, verbose_name='销售日期')),
                ('storage', models.IntegerField(verbose_name='库存数量')),
                ('info', models.TextField(blank=True, null=True, verbose_name='产品信息')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否可见')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_system.Category', verbose_name='分类')),
                ('purchaser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='storage_system.Customer', verbose_name='购买者')),
            ],
            options={
                'verbose_name': '产品',
                'verbose_name_plural': '产品信息',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=32, verbose_name='状态')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否可见')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '状态',
                'verbose_name_plural': '状态',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='标签名')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否可见')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_system.Status', verbose_name='商品状态'),
        ),
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, to='storage_system.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='customer',
            name='tag',
            field=models.ManyToManyField(blank=True, to='storage_system.Tag', verbose_name='标签'),
        ),
    ]
