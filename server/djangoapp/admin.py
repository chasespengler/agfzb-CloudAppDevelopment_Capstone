from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'dealer_id', 'car_type', 'year', 'color']
    search_fields = ['name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = ['CarModelInline']
    list_display = ['name', 'description']
    search_fields = ['name']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
