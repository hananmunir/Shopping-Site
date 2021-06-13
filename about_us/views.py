from django.shortcuts import render

# Create your views here.

# Displays about us page
def about_us_view(request):
    return render(request, 'AboutUs.html')
