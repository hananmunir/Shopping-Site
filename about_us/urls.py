from django.urls import path
from .views import about_us_view

app_name = 'about_us'
urlpatterns = [
    path('', about_us_view, name="About")
]