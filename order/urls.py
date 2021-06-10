from django.urls import path
from .views import *


app_name = "Order"

urlpatterns = [
    path('cart/', cart_view, name='home'),
    path('order_confirmed/', confirmation_view, name= 'order-confirmed'),
    path('update_item/', update_item, name="searched-product-view"),
    path('payment/', payment_view, name="payment-view"),
    path('orders/<int:id>/',order_history_view, name = "order-history-view"),
    path('orders/review/<int:id>',write_review_view, name = "write-review-view"),

]