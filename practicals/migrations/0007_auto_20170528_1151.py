# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('practicals', '0006_auto_20170528_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allsubject',
            old_name='stream',
            new_name='stream_obj',
        ),
        migrations.RenameField(
            model_name='assignment',
            old_name='subject',
            new_name='subject_obj',
        ),
    ]