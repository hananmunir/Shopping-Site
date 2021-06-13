from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
import json
from .models import Product
from order.models import Order,OrderItem
# Create your views here.


# Displays write review page
@login_required()
def write_review_view(request,id):

    #gets the product that has the given id
    product = get_object_or_404(Product, id = id)
    context = {
        'product': product
    }

    return render(request, "Order/review_product.html",context)


# diplays order history
@login_required()
def order_history_view(request,id):

    # gets the Order that has the given id
    order = get_object_or_404(Order,id = id)
    items = order.orderitem_set.all()
    context = {
        'order': order,
        'items': items
    }
    return render(request,'Order/order_history.html', context)


# Logic to update cart
@login_required(redirect_field_name='accounts/login')
def update_item(request):

    #gets data from the cart.js file
    data = json.loads(request.body)

    #gets product id and action
    productId = data['productId']
    action = data['action']

    #gets user and product
    customer = request.user.customer
    product = Product.objects.get(id = productId)

    #gets or creates order and order item
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    #updates cart
    if action == 'add' or action == 'increase':
        orderItem.quantity += 1
    if action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    #deletes a product from cart
    if action == 'delete' or orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item Was Added', safe=False)

#diplays cart
def cart_view(request):

    #authenticates if user is logged in
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete = False)
        items = order.orderitem_set.all()

    #if not logged in, redirects to login
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


#Displays payment view
def payment_view(request):
    return render(request, 'Order/pay.html')

#displays confirmation page
def confirmation_view(request):
    return render(request, 'Order/orderConfirmation.html')
