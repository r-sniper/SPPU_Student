# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 10:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('practicals', '0003_auto_20170528_1009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allsubject',
            old_name='subjects',
            new_name='subject',
        ),
    ]