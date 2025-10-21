from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AircraftViewSet, AirportViewSet, TerminalViewSet, FareTypeViewSet,
    FlightRouteViewSet, FlightLegViewSet, FlightScheduleViewSet,
    FlightClassViewSet, FlightClassFareViewSet, FlightSeatViewSet,
    PassengerViewSet
)

# Create a router and register your viewsets
router = DefaultRouter()

# ---------------------- BASE DATA ----------------------
router.register(r'aircrafts', AircraftViewSet, basename='aircraft')
router.register(r'airports', AirportViewSet, basename='airport')
router.register(r'terminals', TerminalViewSet, basename='terminal')
router.register(r'fare-types', FareTypeViewSet, basename='faretype')

# ---------------------- FLIGHTS ----------------------
router.register(r'flight-routes', FlightRouteViewSet, basename='flightroute')
router.register(r'flight-legs', FlightLegViewSet, basename='flightleg')
router.register(r'flight-schedules', FlightScheduleViewSet, basename='flightschedule')

# ---------------------- CLASSES & FARES ----------------------
router.register(r'flight-classes', FlightClassViewSet, basename='flightclass')
router.register(r'flight-class-fares', FlightClassFareViewSet, basename='flightclassfare')
router.register(r'flight-seats', FlightSeatViewSet, basename='flightseat')

# ---------------------- PASSENGERS ----------------------
router.register(r'passengers', PassengerViewSet, basename='passenger')

# Include router URLs
urlpatterns = [
    path('api/flights/', include(router.urls)),
]
