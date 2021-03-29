from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class Profile(models.Model):
    choices = (('Admin', "Admin"),('User', "User"))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=8 , choices=choices, default="User")
    
    
    def __str__(self):
        return self.user.email

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    quantity= models.IntegerField(default=0)
    choices = (('Active', "Active"),('Inactive', "Inactive"))
    status= models.CharField(max_length=8 , choices=choices, default="Active")
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    item = models.ForeignKey(Products , on_delete=models.CASCADE)
    order_quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.name
    
    def get_total_item_price(self):
        return self.order_quantity * self.item.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    Order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 

    def get_total(self):
        total= 0 
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total