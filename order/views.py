from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
import json
from .models import Product
from order.models import Order,OrderItem
# Create your views here.

@login_required()
def write_review_view(request,id):
    product = get_object_or_404(Product, id = id)
    context = {
        'product': product
    }

    return render(request, "Order/review_product.html",context)

@login_required()
def order_history_view(request,id):
    order = get_object_or_404(Order,id = id)
    items = order.orderitem_set.all()
    context = {
        'order': order,
        'items': items
    }
    return render(request,'Order/order_history.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    if action == 'add' or action == 'increase':
        orderItem.quantity += 1
    if action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if action == 'delete' or orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item Was Added', safe=False)

def cart_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total':0,
            'get_cart_items':0
        }
        redirect('/accounts/login')

    context = {
        'items': items,
        'order': order
    }
    return render(request, 'Order/Cart.html',context)



def payment_view(request):
    return render(request, 'Order/pay.html')

def confirmation_view(request):
    return render(request, 'Order/orderConfirmation.html')
