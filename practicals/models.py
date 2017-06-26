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


class StreamData(models.Model):
    stream = models.CharField(max_length=100)
    year = models.CharField(max_length=5)

    def __str__(self):
        return str(self.id) + " " + self.stream + "-" + self.year


class AllSubject(models.Model):
    stream_obj = models.ForeignKey(StreamData, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return (str(self.id) + " " + self.subject)


class Assignment(models.Model):
    subject_obj = models.ForeignKey(AllSubject, on_delete=models.CASCADE)
    problem_statement = models.TextField(max_length=2500)
    title = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)

    def __str__(self):
        return (self.title + " " + self.filename)


class Quotes(models.Model):
    quote = models.CharField(max_length=2000)
    author = models.CharField(max_length=100,default="Anonymous")
    def __str__(self):
        return (str(self.id) + " " + self.quote)