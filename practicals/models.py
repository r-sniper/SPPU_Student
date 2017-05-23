# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

'''
STRUCTURE

    |- Stream   
    |- Year     
            |-Subject
            |-Assignment Title
            |-Problem Statement
            |-Filename

'''


class Stream_Data(models.Model):
    stream = models.CharField(max_length=100)
    year = models.CharField(max_length=5)

    def __str__(self):
        return (str(self.id) + " " + self.stream + "-" + self.year)


class Subject_Data(models.Model):
    stream_id = models.ForeignKey(Stream_Data, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    assignment_title = models.CharField(max_length=250)
    problem_statement = models.TextField(max_length=2500)
    filename = models.CharField(max_length=20)

    def __str__(self):
        return (str(self.id) + " " + self.subject + " " + self.assignment_title)
