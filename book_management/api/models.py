# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey('self', null=True)

    def __str__(self):
        return '<Category name={}, parent_category={}>'.format(self.name, self.parent_category)

class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    isbn = models.CharField(max_length=100)

    def __str__(self):
        return '<Book title={}, category={}, isbn={}>'.format(self.title, self.category, self.isbn)
    