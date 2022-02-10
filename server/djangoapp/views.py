from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview, CarModel, CarMake
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://a88eec50.us-south.apigw.appdomain.cloud/api/dealership"               
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealership_list"]=dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context={}
    url = "https://a88eec50.us-south.apigw.appdomain.cloud/api/review"
    info_url = "https://a88eec50.us-south.apigw.appdomain.cloud/api/dealership"
    # Get dealers from the URL
    dealer_details = get_dealer_reviews_from_cf(url,dealer_id)

    context["dealer_id"]=dealer_id
    context["reviews"]=dealer_details
    context["dealer_name"] = get_dealers_from_cf(info_url)[dealer_id].full_name
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):    
    context = {}
    if request.method == 'GET':
        url = "https://a88eec50.us-south.apigw.appdomain.cloud/api/dealership"
        carList = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id].full_name,
            "cars": carList
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = {}
            review["name"]=request.user.first_name + " " + request.user.last_name
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("is_purchased" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("-")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]
            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None            
            
            jsonData = json.dumps(review)
            json_payload  = dict()
            json_payload["review"] = review
            json_result = post_request("https://a88eec50.us-south.apigw.appdomain.cloud/api/review", json_payload)
            print(json_result)
            if "error" in json_result:
                context["message"] = "Error occured on submitting a review."
            else:
                context["message"] = "OK"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)