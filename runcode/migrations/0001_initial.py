# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-25 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Learning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('code_language', models.TextField(blank='True', max_length=30)),
                ('code', models.TextField(blank='True', max_length=2000)),
                ('context', models.TextField(blank='True', max_length=4000)),
                ('title', models.TextField(blank='True', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_id', models.TextField(blank='True', max_length=20)),
                ('login_pwd', models.TextField(blank='True', max_length=20)),
                ('login_date', models.DateTimeField(auto_now=True)),
                ('login_error', models.TextField(blank='True')),
            ],
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_user', models.TextField(blank='True', max_length=20)),
                ('run_language', models.TextField(blank='True', max_length=20)),
                ('run_date', models.DateTimeField(auto_now=True)),
                ('code', models.TextField(blank='True', max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(blank='True', max_length=20)),
                ('user_pwd', models.TextField(blank='True', max_length=20)),
                ('user_name', models.TextField(blank='True', max_length=20)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
