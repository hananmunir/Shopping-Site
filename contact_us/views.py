from django.shortcuts import render

# Create your views here.


#Displays contact us page
def contact_us_view(request):
    return render(request,'ContactUs.html')
