from rest_framework import serializers
from models import Category, Book

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
        depth = 1

class BookSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source='category.id')
    class Meta:
        model = Book
        fields = '__all__'
        depth = 0