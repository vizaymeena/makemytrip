from rest_framework import serializers
from decimal import Decimal
from apps.hotels.models import (
    HotelChain, Hotel, HotelImage, Amenity, HotelAmenity,
    RoomType, RoomTypeImage, RoomAmenity, RoomTypeAmenity,
    Room, RoomAvailability, Guest, HotelBooking, BookingRoom
)

# ------------------ Hotel Chain ------------------

class HotelChainSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = HotelChain
        fields = '__all__'

    def validate(self, data):
        # Object-level validation example
        if 'name' in data and 'code' in data:
            if data['name'].lower() == data['code'].lower():
                raise serializers.ValidationError("Name and code should not be identical")
        return data

# ------------------ Hotel Image ------------------

class HotelImageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = HotelImage
        fields = '__all__'

# ------------------ Hotel ------------------

class HotelSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    images = HotelImageSerializer(many=True, required=False)
    
    class Meta:
        model = Hotel
        fields = '__all__'

    def validate(self, data):
        # Object-level validation
        if 'check_in_time' in data and 'check_out_time' in data:
            if data['check_in_time'] >= data['check_out_time']:
                raise serializers.ValidationError("Check-in time must be before check-out time.")
        if 'average_rating' in data:
            if not (0 <= data['average_rating'] <= 5):
                raise serializers.ValidationError("Average rating must be between 0 and 5.")
        return data

    def update(self, instance, validated_data):
        # Conditional update for images
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data is not None:
            # Replace all images if new images provided
            instance.images.all().delete()
            for image in images_data:
                HotelImage.objects.create(hotel=instance, **image)
        return instance

# ------------------ Amenity ------------------

class AmenitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Amenity
        fields = '__all__'

# ------------------ Hotel Amenity ------------------

class HotelAmenitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = HotelAmenity
        fields = '__all__'

# ------------------ Room Type Image ------------------

class RoomTypeImageSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = RoomTypeImage
        fields = '__all__'

# ------------------ Room Type ------------------

class RoomTypeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    images = RoomTypeImageSerializer(many=True, required=False)

    class Meta:
        model = RoomType
        fields = '__all__'

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if images_data is not None:
            instance.images.all().delete()
            for image in images_data:
                RoomTypeImage.objects.create(room_type=instance, **image)
        return instance

# ------------------ Room Amenity ------------------

class RoomAmenitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = RoomAmenity
        fields = '__all__'

# ------------------ Room Type Amenity ------------------

class RoomTypeAmenitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = RoomTypeAmenity
        fields = '__all__'

# ------------------ Room ------------------

class RoomSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = '__all__'

# ------------------ Room Availability ------------------

class RoomAvailabilitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = RoomAvailability
        fields = '__all__'

    def validate(self, data):
        if data['available_rooms'] + data['blocked_rooms'] > data['room_type'].total_rooms:
            raise serializers.ValidationError("Sum of available and blocked rooms cannot exceed total rooms")
        return data

# ------------------ Guest ------------------

class GuestSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Guest
        fields = '__all__'

# ------------------ Hotel Booking ------------------

class HotelBookingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    balance_due = serializers.ReadOnlyField()
    nights_count = serializers.ReadOnlyField()

    class Meta:
        model = HotelBooking
        fields = '__all__'

    def validate(self, data):
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("Check-in date must be before check-out date.")
        if data['total_amount'] < Decimal('0.01'):
            raise serializers.ValidationError("Total amount must be positive.")
        return data

# ------------------ Booking Room ------------------

class BookingRoomSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = BookingRoom
        fields = '__all__'

    def validate(self, data):
        if data['adults'] + data['children'] > data['room_type'].max_occupancy:
            raise serializers.ValidationError("Guest count exceeds room maximum occupancy")
        return data
