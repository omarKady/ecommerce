from collections import namedtuple
from django import forms
from django.contrib import admin
from django.db.models import fields
from django.forms.formsets import all_valid
from .models import Category, Order, Feedback, Product, Customer
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)