# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.generics import ( 
  ListCreateAPIView, RetrieveUpdateDestroyAPIView, 
  ListAPIView, get_object_or_404 
)



from models import Category, Book
from serializers import CategorySerializer, BookSerializer


class CategoryView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        """
        Overrides the default perform_create method
        Save Category's parent_category if parent_category 
        pk is supplied
        """

        parent_category = self.request.data.get('parent_category')
        if not parent_category:
            serializer.save()
        else:
            parent_category = get_object_or_404(Category, pk=parent_category)
            serializer.save(parent_category=parent_category)


class BookView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer 

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryBookView(ListCreateAPIView):
    serializer_class = BookSerializer

    def get_category(self):
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=category_id)
        return category

    def perform_create(self, serializer):
        """
        Overrides the default perform_create method
        Save Book category as specified category 
        """
        category = self.get_category()
        serializer.save(category=category)
    
    def get_queryset(self):
        category = self.get_category()
        return Book.objects.filter(category=category)