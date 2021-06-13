from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User, auth
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout
import datetime

from order.models import Order



# Create your views here.

# view for policies
def policies_view(request): 
    return render(request,'policy.html')


# view for login page
def login_view(request):
    #logs out the current user
    logout(request)
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']

        user = auth.authenticate(username=username, password=password)

        # authenticates a user
        if user is not None:
            auth.login(request, user)

            #if user is admin, redirect to admin panel
            if user.is_staff:
                return redirect('/admin')
            return redirect('/products')
        else:
            messages.info(request, "UserName or password doesnt exist")
            return redirect('/accounts/login')
    else:
        return render(request, 'login.html')


# the personal info page, requires user to be logged in
# in case of not logged in, redirects to login page
@login_required(redirect_field_name = 'login/')
def personal_info_update_view(request):
    customer = request.user.customer
    context = {
        'customer': customer
    }


    #gets all the data through post request
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        #checks if the email is unique
        if Customer.objects.filter(email=email).exists() and email != customer.email:
            messages.info(request, "Email Already Registered")

        else:
            customer.fname = fname
            customer.lname = lname

            customer.email = email
            customer.gender = gender
            customer.save()
            return redirect("../accounts")

    return render(request, "edit_personal_info.html",context)

#form to update address
#requires user to be logged in
@login_required(redirect_field_name = 'login/')
def address_update_view(request):

    customer = request.user.customer
    context = {
        'customer': customer
    }

    #gets info through the post method
    if request.method == 'POST':
        country = request.POST.get('country')
        city = request.POST.get('city')
        area = request.POST.get('area')
        street_address = request.POST.get('address')
        phoneno = request.POST.get('phoneno')

        if len(phoneno) < 7:
            messages.info(request, "Invalid entry in phone number field")
        else:

            #assigings new values
            customer.phone_number = phoneno
            customer.address.country = country
            customer.address.city = city
            customer.address.area = area
            customer.address.street_address = street_address
            customer.save()
        #redirect to accounts page
            return redirect("../accounts")


    return render(request, "edit_address.html",context)


#The user account view
#requires user to be logged in
@login_required(redirect_field_name = 'login/')
def accounts_view(request):
    user = request.user

    #if user is staff redirect to admin panel
    if user.is_staff:
        return redirect('/admin')

    #gets all completed orders and passes them in the context dictionary
    order = Order.objects.filter(customer = user.customer,complete = True )
    context = {
        'user': user,
        'orders' : order
    }
    return render(request, 'account.html',context)

## lets the user loggout
def logout_view(request):
    logout(request)

    return redirect('/accounts/login')

#singup view
def signup_view(request):
    # logs out the current user
    logout(request)

    try:
        #the data is send to backend using post method
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            phoneno = request.POST.get('phoneno')
            birthdate = request.POST.get('birthday')
            date_list = birthdate.split('-')
            birthdate = datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2])).date()
            gender = request.POST.get('gender')
            country = request.POST.get('country')
            city = request.POST.get('city')
            area = request.POST.get('area')
            street_address = request.POST.get('address')
            userName = request.POST.get('userName')
            psw = request.POST.get('psw')
            psw_repeat = request.POST.get('psw-repeat')

            max_age = datetime.date.today() - relativedelta(years=110)
            min_age = datetime.date.today() - relativedelta(years=13)

            #validates if both password are same
            if psw == psw_repeat:
                if birthdate > datetime.date.today():
                    messages.info(request, "Invalid birthdate, if you are not from future :)")
                if max_age > birthdate:
                    messages.info(request, "Invalid birthdate,You cannot be older then 110 years. We hope")
                if min_age < birthdate:
                    messages.info(request, "Invalid birthdate,You should be atleast 13 years old")
                if len(phoneno) < 7:
                    messages.info(request, "Invalid entry in phone number field")
                #validates is username is unique
                if User.objects.filter(username = userName).exists():
                    messages.info(request, "UserName Already Exists, try a different username")
                #validates if email is unique
                elif Customer.objects.filter(email=email).exists():
                    messages.info(request, "Email Already Registered")
                else:
                    #objects are created and saved
                    user = User.objects.create_user(username = userName, password = psw)
                    address = Address.objects.create(country = country,city = city, area = area,street_address = street_address)
                    customer = Customer(user = user,fname = fname,lname = lname,email = email,
                                        phone_number = phoneno,DOB = birthdate,gender = gender, address = address)
                    customer.save()
                    return redirect('/accounts/login')
            else:
                messages.info(request, " Password Doesnt Match")

    except IntegrityError:
        pass

    return render(request, 'signup.html')
