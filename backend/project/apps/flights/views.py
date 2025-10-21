
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    Aircraft, Airport, Terminal, FlightRoute, FlightLeg, FlightSchedule,
    FareType, FlightClass, FlightClassFare, FlightSeat, Passenger
)
from .serializers import (
    AircraftSerializer, AirportSerializer, TerminalSerializer, FlightRouteSerializer,
    FlightLegSerializer, FlightScheduleSerializer, FareTypeSerializer,
    FlightClassSerializer, FlightClassFareSerializer, FlightSeatSerializer, PassengerSerializer
)

# ---------------------- MASTER DATA ----------------------
class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

class TerminalViewSet(viewsets.ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer

class FareTypeViewSet(viewsets.ModelViewSet):
    queryset = FareType.objects.all()
    serializer_class = FareTypeSerializer

# ---------------------- FLIGHTS ----------------------
class FlightRouteViewSet(viewsets.ModelViewSet):
    queryset = FlightRoute.objects.all()
    serializer_class = FlightRouteSerializer

class FlightLegViewSet(viewsets.ModelViewSet):
    queryset = FlightLeg.objects.all()
    serializer_class = FlightLegSerializer

class FlightScheduleViewSet(viewsets.ModelViewSet):
    queryset = FlightSchedule.objects.all()
    serializer_class = FlightScheduleSerializer

# ---------------------- CLASSES & FARES ----------------------
class FlightClassViewSet(viewsets.ModelViewSet):
    queryset = FlightClass.objects.all()
    serializer_class = FlightClassSerializer

class FlightClassFareViewSet(viewsets.ModelViewSet):
    queryset = FlightClassFare.objects.all()
    serializer_class = FlightClassFareSerializer

class FlightSeatViewSet(viewsets.ModelViewSet):
    queryset = FlightSeat.objects.all()
    serializer_class = FlightSeatSerializer

# ---------------------- PASSENGERS ----------------------
class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
