# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-22 11:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppealPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('process', models.TextField()),
                ('result', models.TextField()),
                ('force', models.TextField()),
                ('insTm', models.DateTimeField(auto_now_add=True)),
                ('updTm', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField()),
                ('insTm', models.DateTimeField(auto_now_add=True)),
                ('updTm', models.DateTimeField(auto_now=True)),
                ('appealPoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buono.AppealPoint')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('sortNo', models.IntegerField()),
                ('entryStartDate', models.DateTimeField()),
                ('entryEndDate', models.DateTimeField()),
                ('voteStartDate', models.DateTimeField()),
                ('voteendDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insTm', models.DateTimeField(auto_now_add=True)),
                ('updTm', models.DateTimeField(auto_now=True)),
                ('appealPoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buono.AppealPoint')),
            ],
        ),
    ]
