# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APITestCase

from models import Category, Book

class CategoryTest(APITestCase):
    def test_can_create_category_without_parent(self):
        book_data = {
          'name': 'Science'
        }
        response = self.client.post('/api/categories/', book_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Category.objects.filter(name=book_data.get('name')))

    def test_can_create_category_with_parent_category(self):
        category = Category.objects.create(name='Science')
        sub_category_data = { 'name': 'Biology', 'parent_category': category.pk }
        # Category.objects.create(**sub_category_data)

        response = self.client.post('/api/categories/', data=sub_category_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.filter(name=sub_category_data.get('name'), parent_category=category).exists(), True)

    def test_can_update_category(self):
        initial_category_data = { 'name': 'Science' }
        category = Category.objects.create(**initial_category_data)
        updated_category_data = { 'name': 'Sciences'}
        response = self.client.put('/api/categories/{0}/'.format(category.pk), data=updated_category_data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Category.objects.filter(name=initial_category_data.get('name')).exists())
        self.assertTrue(Category.objects.filter(name=updated_category_data.get('name')).exists())

    def test_can_delete_category(self):
        initial_category_data = { 'name': 'Technology' }
        category = Category.objects.create(**initial_category_data)

        response = self.client.delete('/api/categories/{}/'.format(category.pk))
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Category.objects.filter(name=initial_category_data.get('name')).exists())

    def test_can_retrieve_single_category(self):
        initial_category_data = { 'name': 'Technology' }
        category = Category.objects.create(**initial_category_data)

        response = self.client.get('/api/categories/{}/'.format(category.pk))
        self.assertEqual(response.status_code, 200)

        response_data = response.data
        self.assertEqual(response_data.get('name'), initial_category_data.get('name'))

    def test_can_retrieve_list_of_categories(self):
        category1 = Category.objects.create(name='Science')
        category2 = Category.objects.create(name='Technology')

        response = self.client.get('/api/categories/')
        response_data = response.data

        self.assertIsInstance(response_data, list)      
        self.assertEqual(len(response_data), 2)
        
        category = response_data[0]
        
        self.assertIn(category.get('name'), [category1.name, category2.name])

    def test_create_category_with_empty_name_raises_error(self):
      response = self.client.post('/api/categories/', {})

      self.assertEqual(response.status_code, 400)
      self.assertFalse(Category.objects.all())
  

class BookTest(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Science')
        self.sub_category = Category.objects.create(name='Biology', category=self.category)
    
    def test_can_retrieve_all_books(self):
      book_data = {
        'title': 'Introduction to Chemistry',
        'isbn': 'CHM1001',
        'category': self.category
      }
      book = Book.objects.create(**book_data)

      response = self.client.get('/api/books/')
      self.assertEqual(response.status_code, 200)
      
      response_data = response.data
      self.assertIsInstance(response_data, list)
      self.assertEqual(len(response_data), 1)
      self.assertTrue(Book.objects.filter(title=book_data.get('title')).exists())

    def test_can_create_book_for_cateogry(self):
        book_data = {
          'title': 'Introduction to Science',
          'isbn': 'SCI12345'
        }
        response = self.client.post('/api/categories/{}/books/'.format(self.category.pk), data=book_data)
        self.assertEqual(response.status_code, 201)


    def test_can_create_book_for_sub_cateogry(self):
        book_data = {
          'title': 'Introduction to Biology',
          'isbn': 'BIO12345'
        }
        response = self.client.post('/api/categories/{}/books/'.format(self.sub_category.pk), data=book_data)
        self.assertEqual(response.status_code, 201)
      
    def test_create_book_with_no_title_raises_error(self):
        book_data = {
          'isbn': 'SCI12345'
        }
        response = self.client.post('/api/categories/{}/books/'.format(self.category.pk), data=book_data)
        self.assertEqual(response.status_code, 400)

    def test_create_book_with_no_isbn_raises_error(self):
        book_data = {
          'title': 'Introduction to Science'
        }
        response = self.client.post('/api/categories/{}/books/'.format(self.category.pk), data=book_data)
        self.assertEqual(response.status_code, 400)

