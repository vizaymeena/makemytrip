from django.contrib import admin
from apps.hotels.models import *
admin.site.register([HotelChain,Hotel,HotelImage,Amenity,HotelAmenity,RoomType,RoomTypeImage,RoomAmenity,RoomTypeAmenity,Room,RoomAvailability,Guest,HotelBooking,BookingRoom])