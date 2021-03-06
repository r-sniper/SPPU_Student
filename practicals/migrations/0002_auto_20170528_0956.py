# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 09:56
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('practicals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_statement', models.TextField(max_length=2500)),
                ('title', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practicals.AllSubject')),
            ],
        ),
        migrations.CreateModel(
            name='MasterTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_stream', models.IntegerField()),
                ('id_subject', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StreamData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='subject_data',
            name='stream_id',
        ),
        migrations.DeleteModel(
            name='Stream_Data',
        ),
        migrations.DeleteModel(
            name='Subject_Data',
        ),
    ]
