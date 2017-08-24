# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    isbn = models.CharField(max_length=100)
    