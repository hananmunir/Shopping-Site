from django.shortcuts import render
from product.models import Product

# Create your views here.
def home_view(request):
    products = Product.objects.filter(top_product = True)

    context = {
        'products': products
    }
    return render(request, 'home.html', context)

