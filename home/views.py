from django.shortcuts import render
from product.models import Product

# Create your views here.

#displays home page
def home_view(request):
    #set of all top products
    products = Product.objects.filter(top_product = True)

    context = {
        'products': products
    }
    return render(request, 'home.html', context)

