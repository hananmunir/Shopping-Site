from django.urls import path
from .views import *


app_name = 'Products'

urlpatterns =[
    path('products/', product_view, name="product-view"),
    path('products/search/', search_product_view, name="searched-product-view"),
    path('products/<int:id>/', product_detialed_view, name="product-detail-view"),

]