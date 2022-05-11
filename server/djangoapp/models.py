from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length = 50, null = False)
    description = models.CharField(max_length = 400)

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(max_length=5)
    name = models.CharField(max_length = 50, null = False)
    my_choices = [('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('WAGON', 'Wagon')]
    car_type = models.CharField(max_length=10, choices = my_choices)
    year = models.DateField()
    color = models.CharField(max_length=20)

    def __str__(self):
        return "Name: " + self.name + " Make: " + self.make + " Color: " + self.color + \
        " Type: " + self.car_type + " Year: " + self.year + " ID: " + self.dealer_id


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview():
    def __init__(self, dealership, name, purchase, review, date, make, model, year, sentiment, my_id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = date
        self.car_make = make
        self.car_model = model
        self.car_year = year
        self.sentiment = sentiment
        self.id = my_id
