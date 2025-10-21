from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HotelChainViewSet, HotelViewSet, HotelImageViewSet,
    AmenityViewSet, HotelAmenityViewSet,
    RoomTypeViewSet, RoomViewSet,
    GuestViewSet, HotelBookingViewSet
)

router = DefaultRouter()
router.register(r'hotel-chains', HotelChainViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'hotel-images', HotelImageViewSet)
router.register(r'amenities', AmenityViewSet)
router.register(r'hotel-amenities', HotelAmenityViewSet)
router.register(r'room-types', RoomTypeViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'guests', GuestViewSet)
router.register(r'hotel-bookings', HotelBookingViewSet)

urlpatterns = [
    path('api/hotels/', include(router.urls)),
]
