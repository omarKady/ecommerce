from django.db import models
from django.db.models import fields
from django.db.models.fields import files
from rest_framework import serializers
from core.models import Customer, Feedback, Order, Product

# Serializer for read (list) products
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    categ_id = serializers.CharField(source='categ_id.name')

# Serializer for create products
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

# Serializer to view manytomany data in Order list endpoint
class ProductRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, value):
        return value.name


class OrderSerializer(serializers.ModelSerializer):
    products = ProductRelatedSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
    customer = serializers.CharField(source='customer.get_name')


class FeedbackSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
