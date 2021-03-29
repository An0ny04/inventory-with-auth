from django.contrib import admin
from .models import Products , Order , OrderItem , Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)