from django.db import models
from django.shortcuts import reverse


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=256, null = True)
    price = models.FloatField()
    discount = models.IntegerField(default= 5,null=True)
    special_note = models.CharField(max_length=256, blank=True , null=True)
    specifications = models.CharField(max_length = 512, null=True)
    description = models.CharField(max_length=512, null = True)
    in_stock = models.BooleanField(default=True, null = True)
    top_product = models.BooleanField(default=False, null=True)
    image = models.ImageField(null= True)


    @property
    def get_rating(self):
        orders = self.orderitem_set.all()
        rating = orders.rating

        if rating is None or rating <= 0:
            return 3;
        return rating


    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''

        return str(url)
    @property
    def get_absolute_url(self):
        return reverse('Products:product-detail-view',kwargs= {'id' : self.id})