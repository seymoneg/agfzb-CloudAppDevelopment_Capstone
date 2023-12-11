from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect("djangoapp:index")
    return redirect("djangoapp:index")


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logger.info(f"Logout the user: {request.user.username}")
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user registered successfully")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.is_superuser = True
            user.is_staff=True
            user.save()  
            login(request, user)
            messages.success(request, "User registered successfully!")
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "The user already exists.")
            return redirect("djangoapp:register")

# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        dealerships = get_dealers_from_cf(url)
        
        # context = {}
        # context["dealerships"] = dealerships
        context = {"dealership_list": dealerships}
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        url = "http://127.0.0.1:5000/api/get_reviews"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, id=id)
        # Concat all dealer's short name
        dealer_names = " ".join([dealer.name for dealer in reviews])
        # Return a list of dealer short name
        print(reviews)
        return render(request,"djangoapp/dealer_details.html",{"reviews": reviews, "id": id},)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

