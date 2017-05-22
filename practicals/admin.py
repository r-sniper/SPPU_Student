# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Stream_Data, Subject_Data

admin.site.register(Stream_Data)
admin.site.register(Subject_Data)
