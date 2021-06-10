from django.shortcuts import render, redirect,get_object_or_404
from .models import Product
from django.http import JsonResponse
import json
from django.contrib import messages
# Create your views here.

def product_detialed_view(request,id):
    product = get_object_or_404(Product,id = id)
    context = {
        'product' : product
    }
    
    return render(request,'Product/product_detailed_view.html',context)
def product_view(request):
    product = Product.objects.all()


    context = {
        'products': product
    }

    return render(request,'Product/search_product.html',context)


def search_product_view(request):
    products = Product.objects.all()
    query = request.GET.get('search')

    quered_product = []
    for product in products:
        if query.lower() in product.title.lower():
            quered_product.append(product)

    if len(quered_product) == 0:
        messages.info(request, "Sorry! We Could not find any relevant product. Feel free to check our other Products")
    context = {
        'products': quered_product
    }
    return render(request,'Product/product_view.html',context)
