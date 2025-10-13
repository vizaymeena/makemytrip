from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# Service Provider Model
from apps.common.models import Airline



# Create your models here.

# Aircraft Type Small,Big 
class Aircraft(models.Model):
    airline = models.ForeignKey(Airline,on_delete=models.CASCADE)
    total_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    economy_seats = models.PositiveIntegerField(default=0)
    business_seats = models.PositiveIntegerField(default=0)
    firstclass_seats = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True,db_index=True)

    class Meta:
        ordering = ['airline']

    def __str__(self):
        return f"( aircraft name is {self.airline})"

# Airports for flights & Stops
class Airport(models.Model):
    countryChoices = [("IND","India"),("SING","Singapore"),("JPN","Japan")]
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)  # e.g., DEL, BLR
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=200,choices=countryChoices)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_international = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Terminal(models.Model):
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="terminals")
    name = models.CharField(max_length=50)  # e.g., Terminal 1, Terminal 2
    code = models.CharField(max_length=10, blank=True, null=True)  # optional terminal code
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("airport", "name")
        ordering = ["airport", "name"]

    def __str__(self):
        return f"{self.airport.code} - {self.name}"

# Permanent Flight Route For Journey
class FlightRoute(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    flight_number = models.CharField(max_length=10)
    origin = models.ForeignKey(Airport, related_name="departures", on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, related_name="arrivals", on_delete=models.CASCADE)
    is_direct = models.BooleanField(default=False)
    operational_days = models.PositiveIntegerField(default=7)  # days in a week 0-7
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.airline.code} {self.flight_number}: {self.origin.code} → {self.destination.code}"


# FLight Stops Between Journey
class FlightLeg(models.Model):
    route = models.ForeignKey(FlightRoute, on_delete=models.CASCADE, related_name="legs")
    stop_order = models.PositiveIntegerField()  # 1,2,3 etc.
    origin = models.ForeignKey(Airport, related_name="leg_departures", on_delete=models.CASCADE)
    destination = models.ForeignKey(Airport, related_name="leg_arrivals", on_delete=models.CASCADE)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ["stop_order"]

    def __str__(self):
        return f"{self.route.flight_number} Stop {self.stops_order}: {self.origin.code} → {self.destination.code}"


# Which Flight is Schedule for the date
class FlightSchedule(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("delayed", "Delayed"),
        ("cancelled", "Cancelled"),
        ("rescheduled", "Rescheduled"),
    ]
     
    flight_leg = models.ForeignKey(FlightLeg, on_delete=models.CASCADE, related_name="schedules")
    flight_date = models.DateField()
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    departure_time = models.TimeField()  # exact time for that schedule
    arrival_time = models.TimeField()

    status = models.CharField(max_length=12,choices=STATUS_CHOICES,default="scheduled",help_text="Current status of the flight")

    delay_minutes = models.PositiveIntegerField( blank=True, null=True, help_text="If delayed, number of minutes delayed" )

    rescheduled_to = models.DateTimeField(blank=True, null=True,help_text="New datetime if flight is rescheduled")

    def __str__(self):
        return f"{self.flight_leg.route.flight_number} on {self.flight_date}"

# Fare options Saver , Super Saver & MMT Special
class FareType(models.Model):
    name = models.CharField(max_length=50)  # e.g., Saver, Super Saver, MMT Special
    description = models.TextField(blank=True)
    
    # Perks
    is_refundable = models.BooleanField(default=False)
    seat_selection = models.BooleanField(default=False)
    meal_included = models.BooleanField(default=False)
    baggage_allowance_kg = models.PositiveIntegerField(default=0)
    extra_baggage_allowed = models.BooleanField(default=False)
    priority_boarding = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    

# Scheduled Flight Class (Economy, Business, Premium)
class FlightClass(models.Model):
    scheduled_flight = models.ForeignKey(FlightSchedule, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=20)  # Economy, Business, Premium
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.schedule.flight_leg.route.flight_number} - {self.name}"

# 
class FlightClassFare(models.Model):
    flight_class = models.ForeignKey(FlightClass, on_delete=models.CASCADE, related_name="fares")
    fare_type = models.ForeignKey(FareType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ("flight_class", "fare_type")
    
    def __str__(self):
        return f"{self.flight_class.name} - {self.fare_type.name}"


# FlightSeat for each class
class FlightSeat(models.Model):
    flight_class = models.ForeignKey(FlightClass, on_delete=models.CASCADE, related_name="seats")
    flight_class_fare = models.ForeignKey(FlightClassFare,on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.flight_class.schedule.flight_leg.route.flight_number} - {self.seat_number} ({self.flight_class.name})"


# Passenger Travelling
class Passenger(models.Model):
    PASSENGER_TYPE_CHOICES = [
        ("adult", "Adult"),
        ("child", "Child"),
        ("infant", "Infant"),
    ]

    passenger_type = models.CharField(max_length=10,choices=PASSENGER_TYPE_CHOICES,default="adult")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    # Link child/infant to adult
    guardian = models.ForeignKey("self",on_delete=models.SET_NULL,blank=True,null=True,related_name="dependents",limit_choices_to={"passenger_type": "adult"})

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.passenger_type})"
