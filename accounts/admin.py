from django.contrib import admin

# Register your models here.
from .models import Address, Customer
admin.site.register(Address)
admin.site.register(Customer)
