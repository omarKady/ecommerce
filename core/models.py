from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields.related import OneToOneField
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
# Create your models here.
CustomUSer = get_user_model()
class Customer(models.Model):
    user = models.OneToOneField(CustomUSer, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    address = models.CharField(max_length=50)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_email(self):
        return self.user.email
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return self.user.first_name

class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=40)
    price = models.PositiveIntegerField(null=False, blank=False)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='products')
    quantity = models.IntegerField()
    color = models.CharField(max_length=20)
    categ_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    ordered_quantity = models.PositiveIntegerField(default=1)


class Feedback(models.Model):
    name = models.CharField(max_length=40)
    feedback = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=250, default=None)

    def __str__(self):
        return self.name