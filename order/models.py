from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import Customer
from product.models import Product
from django.shortcuts import reverse
import datetime
# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True , null=True )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_ID = models.CharField(max_length= 256, default= datetime.datetime.now().timestamp(), null = True)

    @property
    def get_absolute_url(self):
        return reverse('Order:order-history-view',kwargs= {'id' : self.id})

    @property
    def get_total_discount(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.get_discount for items in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.get_total for items in orderitems])
        return total

    @property
    def get_cart_total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.get_total for items in orderitems]) - sum([items.get_discount for items in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.quantity for items in orderitems])
        return total



    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete= models.SET_NULL,blank=True, null=True)
    quantity = models.IntegerField(default= 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def rating(self):
        reviews = OrderItem.Product_reviews_set.all()
        length = len(reviews)
        rating = (sum([review.rating for review in reviews]))/length
        return rating

    @property
    def get_total(self):
        total = (self.product.price * self.quantity)

        return int(total)
    @property
    def get_discount(self):
        discount = (self.product.price * self.quantity * self.product.discount/100)
        return discount

class Product_Review(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete = models.SET_NULL, blank=True,null= True)
    review = models.CharField(max_length= 720, blank=True, null= True)
    rating = models.IntegerField(
         null = True,
        validators= [
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    isAnonymous = models.BooleanField(default= False)

class Shipping_Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_address(self):
        return self.customer.get_address()






