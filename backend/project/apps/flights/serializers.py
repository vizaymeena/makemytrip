from rest_framework import serializers
from datetime import date, datetime, time

from .models import (
    Aircraft, Airport, Terminal, FlightRoute, FlightLeg, FlightSchedule,
    FareType, FlightClass, FlightClassFare, FlightSeat, Passenger
)


# ---------------------- AIRCRAFT ----------------------
class AircraftSerializer(serializers.ModelSerializer):
    airline_name = serializers.CharField(source='airline.name', read_only=True)

    class Meta:
        model = Aircraft
        fields = '__all__'
        read_only_fields = ['id','airline']

    def validate(self, data):
        econ = data.get('economy_seats') or 0
        prem = data.get('premium_seats') or 0
        bus = data.get('business_seats') or 0
        total = data.get('total_seats')
      
        if any(seat < 0 for seat in [econ, prem, bus]):
            raise serializers.ValidationError("Seat counts cannot be negative.")

        if total is not None and total <= 0:
            raise serializers.ValidationError("Total seats must be greater than zero.")

        if total and (econ + prem + bus) > total:
            raise serializers.ValidationError("Sum of seat classes cannot exceed total seats.")
    
        if (econ or prem or bus) and total and (econ + prem + bus) != total:
            raise serializers.ValidationError("Sum of seat classes must equal total seats.")

        return data

         

# ---------------------- AIRPORT ----------------------

class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = '__all__'
        read_only_fields =['id']

    def validate_code(self, value):
        value = value.upper()
        qs = Airport.objects.filter(code=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Airport code must be unique globally.")
        return value

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")
        return value

    def validate(self, data):
        name = data.get('name')
        city = data.get('city')
        country = data.get('country')
        is_international = data.get('is_international')

        if not name or not name.strip():
            raise serializers.ValidationError({"name": "Airport name cannot be empty."})
        if not city or not city.strip():
            raise serializers.ValidationError({"city": "City cannot be empty."})

        if country != 'IND' and not is_international:
            raise serializers.ValidationError({
                "is_international": "Airports outside India must have is_international=True."
            })

        return data



# ---------------------- TERMINAL ----------------------

class TerminalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Terminal
        fields = '__all__'
        read_only_fields =['id','airport']


    def validate(self, data):
        name = data.get("name")
        code = data.get("code")
        airport = data.get("airport")
       
        if not name or not name.strip():
            raise serializers.ValidationError({"name": "Terminal name cannot be empty."})

        if not airport.is_active:
            raise serializers.ValidationError({"airport": "Cannot assign a terminal to an inactive airport."})

        if code:
            code = code.upper()
            qs = Terminal.objects.filter(code=code, airport=airport)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"code": f"Terminal code '{code}' already exists for this airport."}
                )
            data["code"] = code  

        return data

# ---------------------- FLIGHT ROUTE ----------------------
class FlightRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlightRoute
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        airline = data.get('airline')
        flight_number = data.get('flight_number')
        origin = data.get('origin')
        destination = data.get('destination')
        operational_days = data.get('operational_days')
        is_direct = data.get('is_direct')

        errors = {}

        if origin == destination:
            errors['destination'] = "Destination airport cannot be the same as origin."

        if hasattr(airline, 'is_active') and not airline.is_active:
            errors['airline'] = "Cannot create a flight route for an inactive airline."

        qs = FlightRoute.objects.filter(airline=airline, flight_number=flight_number)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            errors['flight_number'] = f"Flight number '{flight_number}' already exists for this airline."

        if operational_days < 1 or operational_days > 7:
            errors['operational_days'] = "Operational days must be between 1 and 7."

        if errors:
            raise serializers.ValidationError(errors)

        return data

# ---------------------- FLIGHT LEG ----------------------

class FlightLegSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlightLeg
        fields = '__all__'
        read_only_fields = ['id', 'route']

    def validate(self, data):
        route = data.get('route')
        stop_order = data.get('stop_order')
        origin = data.get('origin')
        destination = data.get('destination')
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')
        duration_minutes = data.get('duration_minutes')

        errors = {}

        # Origin and destination cannot be the same
        if origin == destination:
            errors['destination'] = "Destination airport cannot be the same as origin."

        # Stop order must be positive
        if stop_order < 1:
            errors['stop_order'] = "Stop order must be a positive integer."

        # Departure must be before arrival
        if departure_time >= arrival_time:
            errors['arrival_time'] = "Arrival time must be after departure time."

        # Duration check (optional)
        if duration_minutes is not None:
            calculated_duration = int((datetime.combine(datetime.today(), arrival_time) - 
                                       datetime.combine(datetime.today(), departure_time)).total_seconds() / 60)
            if duration_minutes != calculated_duration:
                errors['duration_minutes'] = f"Duration_minutes does not match the difference between departure and arrival ({calculated_duration} mins)."

        # 5️Unique stop_order per route
        qs = FlightLeg.objects.filter(route=route, stop_order=stop_order)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            errors['stop_order'] = f"Stop order {stop_order} already exists for this route."

        if errors:
            raise serializers.ValidationError(errors)

        return data

# ---------------------- FLIGHT SCHEDULE ----------------------

class FlightScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlightSchedule
        fields = '__all__'
        read_only_fields = ['id', 'flight_leg'] 

    def validate(self, data):
        flight_leg = data.get('flight_leg')
        flight_date = data.get('flight_date')
        aircraft = data.get('aircraft')
        departure_time = data.get('departure_time')
        arrival_time = data.get('arrival_time')
        status = data.get('status')
        delay_minutes = data.get('delay_minutes')
        rescheduled_to = data.get('rescheduled_to')

        errors = {}

        # Arrival must be after departure
        if departure_time >= arrival_time:
            errors['arrival_time'] = "Arrival time must be after departure time."

        # Flight date cannot be in the past
        if flight_date < date.today():
            errors['flight_date'] = "Flight date cannot be in the past."

        # Aircraft must be active
        if not aircraft.is_active:
            errors['aircraft'] = "Cannot assign an inactive aircraft to a schedule."

        # Delay_minutes only valid if status is "delayed"
        if delay_minutes is not None and status != "delayed":
            errors['delay_minutes'] = "Delay minutes can only be set if status is 'delayed'."

        # rescheduled_to only valid if status is "rescheduled"
        if rescheduled_to is not None and status != "rescheduled":
            errors['rescheduled_to'] = "Rescheduled datetime can only be set if status is 'rescheduled'."

        # Optional: Prevent overlapping schedule for same aircraft on same date
        overlapping_qs = FlightSchedule.objects.filter(
            flight_date=flight_date,
            aircraft=aircraft
        )
        if self.instance:
            overlapping_qs = overlapping_qs.exclude(pk=self.instance.pk)

        for schedule in overlapping_qs:
            existing_departure = datetime.combine(schedule.flight_date, schedule.departure_time)
            existing_arrival = datetime.combine(schedule.flight_date, schedule.arrival_time)
            new_departure = datetime.combine(flight_date, departure_time)
            new_arrival = datetime.combine(flight_date, arrival_time)
            if (new_departure < existing_arrival) and (new_arrival > existing_departure):
                errors['aircraft'] = f"Aircraft '{aircraft}' has an overlapping flight on this date."

        if errors:
            raise serializers.ValidationError(errors)

        return data
    

# ---------------------- FARE TYPE ----------------------

class FareTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FareType
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        errors = {}

        name = data.get('name')
        baggage_allowance = data.get('baggage_allowance_kg', 0)
        extra_baggage_allowed = data.get('extra_baggage_allowed', False)

        # Name must be provided
        if not name or not name.strip():
            errors['name'] = "Fare type name cannot be empty."

        # Name must be unique
        qs = FareType.objects.filter(name__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            errors['name'] = f"Fare type '{name}' already exists."

        # Extra baggage logic
        if extra_baggage_allowed and baggage_allowance == 0:
            errors['extra_baggage_allowed'] = "Extra baggage cannot be allowed if baggage allowance is zero."

        if errors:
            raise serializers.ValidationError(errors)

        return data

# ---------------------- FLIGHT CLASS ----------------------

class FlightClassSerializer(serializers.ModelSerializer):

    ALLOWED_CLASSES = ["Economy", "Business", "Premium"]
    class Meta:
        model = FlightClass
        fields = '__all__'
        read_only_fields = ['id', 'scheduled_flight']

    def validate(self, data):
        scheduled_flight = data.get('scheduled_flight')
        name = data.get('name')
        capacity = data.get('capacity')

        errors = {}

        # Name must be provided and valid
        if not name or not name.strip():
            errors['name'] = "Flight class name cannot be empty."
        elif name not in self.ALLOWED_CLASSES:
            errors['name'] = f"Flight class name must be one of {self.ALLOWED_CLASSES}."

        # Capacity must be positive
        if capacity is None or capacity <= 0:
            errors['capacity'] = "Capacity must be a positive integer."

        # Name must be unique per scheduled flight
        qs = FlightClass.objects.filter(scheduled_flight=scheduled_flight, name=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            errors['name'] = f"'{name}' class already exists for this flight schedule."

        if errors:
            raise serializers.ValidationError(errors)

        return data
    
# ---------------------- FLIGHT CLASS FARE ----------------------

class FlightClassFareSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlightClassFare
        fields = '__all__'
        read_only_fields = ['id', 'flight_class']

    def validate(self, data):
        flight_class = data.get('flight_class')
        fare_type = data.get('fare_type')
        price = data.get('price')

        errors = {}

        # Price must be positive
        if price is None or price <= 0:
            errors['price'] = "Price must be a positive number."

        # Unique combination of flight_class and fare_type
        qs = FlightClassFare.objects.filter(flight_class=flight_class, fare_type=fare_type)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            errors['fare_type'] = f"The fare type '{fare_type}' already exists for flight class '{flight_class}'."

        if errors:
            raise serializers.ValidationError(errors)

        return data

# ---------------------- FLIGHT SEAT ----------------------

class FlightSeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlightSeat
        fields = '__all__'
        read_only_fields = ['id', 'flight_class', 'flight_class_fare']

    def validate(self, data):
        flight_class = data.get('flight_class')
        flight_class_fare = data.get('flight_class_fare')
        seat_number = data.get('seat_number')

        errors = {}

        # Seat number must be provided
        if not seat_number or not seat_number.strip():
            errors['seat_number'] = "Seat number cannot be empty."

        # Seat number must be unique per flight_class
        qs = FlightSeat.objects.filter(flight_class=flight_class, seat_number=seat_number)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            errors['seat_number'] = f"Seat '{seat_number}' already exists for this flight class."

        # flight_class_fare must belong to the same flight_class
        if flight_class_fare.flight_class != flight_class:
            errors['flight_class_fare'] = "Selected fare does not belong to this flight class."

        if errors:
            raise serializers.ValidationError(errors)

        return data

# ---------------------- PASSENGER ----------------------

class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = '__all__'
        read_only_fields = ['id'] 

    def validate(self, data):
        passenger_type = data.get('passenger_type')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        guardian = data.get('guardian')

        errors = {}

        # First and last names cannot be empty
        if not first_name or not first_name.strip():
            errors['first_name'] = "First name cannot be empty."
        if not last_name or not last_name.strip():
            errors['last_name'] = "Last name cannot be empty."

        #  Passenger type must be valid
        if passenger_type not in [choice[0] for choice in Passenger.PASSENGER_TYPE_CHOICES]:
            errors['passenger_type'] = f"Invalid passenger type '{passenger_type}'."

        #  Guardian rules
        if passenger_type in ['child', 'infant'] and not guardian:
            errors['guardian'] = "Child or infant must have a guardian assigned."
        if passenger_type == 'adult' and guardian is not None:
            errors['guardian'] = "Adult passenger cannot have a guardian."

        if errors:
            raise serializers.ValidationError(errors)

        return data