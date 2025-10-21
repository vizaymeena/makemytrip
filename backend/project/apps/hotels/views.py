

from rest_framework import viewsets
from .models import (
    HotelChain, Hotel, HotelImage, Amenity, HotelAmenity,
    RoomType, RoomTypeImage, Room, Guest, HotelBooking, BookingRoom
)
from .serializers import (
    HotelChainSerializer, HotelSerializer, HotelImageSerializer,
    AmenitySerializer, HotelAmenitySerializer,
    RoomTypeSerializer, RoomTypeImageSerializer, RoomSerializer,
    GuestSerializer, HotelBookingSerializer, BookingRoomSerializer
)

# Create your views here.

class HotelChainViewSet(viewsets.ModelViewSet):
    queryset = HotelChain.objects.all()
    serializer_class = HotelChainSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelImageViewSet(viewsets.ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

class HotelAmenityViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenity.objects.all()
    serializer_class = HotelAmenitySerializer

class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class HotelBookingViewSet(viewsets.ModelViewSet):
    queryset = HotelBooking.objects.all()
    serializer_class = HotelBookingSerializer
