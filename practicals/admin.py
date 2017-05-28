# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import StreamData, AllSubject, Assignment

admin.site.register(StreamData)
admin.site.register(AllSubject)
admin.site.register(Assignment)
