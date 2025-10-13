from django.contrib import admin

# Register your models here.
from apps.flights.models import * 

admin.site.register([Aircraft,Airport,Terminal,FlightRoute,FlightLeg,FlightClass,FlightClassFare,FlightSchedule,FlightSeat,FareType,Passenger])