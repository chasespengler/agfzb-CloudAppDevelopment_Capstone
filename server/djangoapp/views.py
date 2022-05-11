from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context["message"]= "Invalid username or password, try again."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'django/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('django:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        try:
            User.objects.get(username=username)
            context["message"] = "Username already exists. Please pick a unique username."
            return render(request, 'djangoapp/registration.html', context)
        except:
            password = request.POST['password']
            first = request.POST['firstname']
            last = request.POST['lastname']
            user = User.objects.create_user(username = username, first_name = first, last_name = last, password = password)
            login(request, user)
            return redirect('djangoapp:index')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "us-south.cf.appdomain.cloud/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    url = "chasespengl.us-south.cf.appdomain.cloud/api/review"
    info_url = "chasespengl.us-south.cf.appdomain.cloud/api/dealership"
    reviews = get_dealer_reviews_from_cf(url, dealer_id)

    context["dealer_id"]=dealer_id
    context["reviews"]=reviews
    context["dealer_name"] = get_dealers_from_cf(info_url)[dealer_id].full_name
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):    
    context = {}
    if request.method == 'GET':
        url = "chasespengl.us-south.cf.appdomain.cloud/api/dealership"
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id].full_name,
            "cars": cars
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["purchase"] = request.POST["purchase"]
            if review["purchase"]:
                review["purchase_date"] = request.POST["purchase_date"] 
                review["car_make"] = request.POST["car_make"]
                review["car_model"] = request.POST["car_model"]
                review["car_year"] = request.POST["car_year"]
            else:
                review["purchase_date"] = "na"   
                review["car_make"] = "na"   
                review["car_model"] = "na"   
                review["car_year"] = "na"            
            
            json_payload = {"review": review}
            json_result = post_request("chasespengl.us-south.cf.appdomain.cloud/api/review", json_payload)
            if "error" in json_result:
                context["message"] = "Review not submitted, try again."
            else:
                context["message"] = "OK"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

