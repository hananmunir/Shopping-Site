from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Address(models.Model):
    country = models.CharField(max_length= 60, null=True)
    city = models.CharField(max_length = 60, null=True ,blank=True)
    area = models.CharField(max_length= 120, null=True)
    street_address = models.CharField(max_length= 120, null=True)

    def __str__(self):
        if self.city is None:
            return str(self.street_address) + ', '  + str(self.area) + ', ' + str(self.country)
        return str(self.street_address) + ', '  + str(self.area) + ', ' + str(self.city) + ', ' + str(self.country)

class Customer(models.Model):
    display_image = models.ImageField(null= True, blank= True)
    user = models.OneToOneField(User, on_delete= models.CASCADE, null = True, blank= True)
    fname = models.CharField(max_length=50 , null= True)
    lname = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length = 256, null = True)
    phone_number = models.CharField(max_length= 15, null = True, blank = True)
    DOB = models.DateField()
    gender = models.CharField(max_length = 6, null = True)
    address = models.ForeignKey(Address, on_delete= models.CASCADE, null=True ,blank=True)


    def __str__(self):
        return self.user.username

    def get_address(self):
        return str(self.address)
    @property
    def get_name(self):
        return str(self.fname) + " " + str(self.lname)
    @property
    def imageURL(self):
        try:
            url = self.display_image.url
        except:
            url = ''

        return url






