from django.contrib import admin
from .models import Category, Order, Feedback, Product, Customer
# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Product)
admin.site.register(Order)