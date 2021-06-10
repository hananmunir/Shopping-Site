from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, Shipping_Address, Product_Review
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product_Review)
admin.site.register(Shipping_Address)
