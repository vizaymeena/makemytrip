from django.db import models
from apps.common.models import ServiceProvider
# Create your models here.


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from decimal import Decimal


# ---------------------- Hotel Group ----------------------

class HotelChain(models.Model):
    "Hotel Group"
    name = models.CharField(max_length=100, unique=True, db_index=True)
    code = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to='hotel_media/%Y/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = _('Hotel Chain')
    
    def __str__(self):
        return self.name

# ---------------------- Hotel  ----------------------

class Hotel(models.Model):
    """Main hotel/property information"""
    service_provider = models.ForeignKey(ServiceProvider,on_delete=models.CASCADE)
    chain = models.ForeignKey( HotelChain,  on_delete=models.SET_NULL,  null=True,  blank=True, related_name='hotels' )

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=250, unique=True, db_index=True)
    
    # Star Rating
    STAR_RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Star'),
        (3, '3 Star'),
        (4, '4 Star'),
        (5, '5 Star'),
    ]
    star_rating = models.IntegerField( choices=STAR_RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Official star rating"
    )
    
    # Location
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    pincode = models.CharField(max_length=10)
        
    # Distance info
    distance_from_city_center_km = models.DecimalField( max_digits=6, decimal_places=2, null=True, blank=True, help_text="Distance from city center in KM" )
    distance_from_airport_km = models.DecimalField( max_digits=6, decimal_places=2, null=True, blank=True )
    
    # Contact
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50,blank=True ,null=True)
    
    # Policy
    check_in_time = models.TimeField(default='14:00:00')
    check_out_time = models.TimeField(default='11:00:00')
    cancellation_policy = models.TextField(
        help_text="Cancellation and refund policy"
    )
    child_policy = models.TextField( blank=True, null=True, help_text="Age limits and pricing for children" )
    pet_policy = models.TextField(blank=True, null=True)
    
    # Description
    description = models.TextField(help_text="Main description")
    short_description = models.CharField( max_length=500, blank=True, null=True, help_text="Brief tagline/description" )
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    
    # Ratings
    average_rating = models.DecimalField( max_digits=3, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0), MaxValueValidator(5)])

    total_reviews = models.PositiveIntegerField(default=0)
    
    # Rooms
    total_rooms = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-is_featured', 'name']
        verbose_name = _('Hotel')
        verbose_name_plural = _('Hotels')
        indexes = [
            models.Index(fields=['city', 'is_active']),
            models.Index(fields=['name', 'city']),
            models.Index(fields=['-average_rating']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.city}"


# ------------------- Hotel Images --------------------

class HotelImage(models.Model):
    """Hotel property images"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotels/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    
    IMAGE_TYPE_CHOICES = [
        ('exterior', 'Exterior'),
        ('lobby', 'Lobby'),
        ('room', 'Room'),
        ('restaurant', 'Restaurant'),
        ('view', 'View'),
        ('other', 'Other'),
    ]
    image_type = models.CharField( max_length=20, choices=IMAGE_TYPE_CHOICES, default='other' )
    
    class Meta:
        ordering = ['hotel', 'display_order']
        verbose_name = _('Hotel Image')
        verbose_name_plural = _('Hotel Images')
    
    def __str__(self):
        return f"{self.hotel.name} - {self.image_type}"


# ------------------- Hotel Amenities ------------------------

class Amenity(models.Model):
    """Master list of amenities"""
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Icon class or emoji")
    
    CATEGORY_CHOICES = [
        ('basic', 'Basic'),
        ('comfort', 'Comfort'),
        ('dining', 'Dining'),
        ('wellness', 'Wellness & Fitness'),
        ('business', 'Business'),
        ('entertainment', 'Entertainment'),
        ('safety', 'Safety & Security'),
        
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='basic')
    is_popular = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = _('Amenity')
        verbose_name_plural = _('Amenities')
    
    def __str__(self):
        return self.name

class HotelAmenity(models.Model):
    """Junction table for hotel amenities"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_amenities')
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    is_free = models.BooleanField(default=True)
    additional_charge = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Additional charge if not free"
    )
    
    class Meta:
        unique_together = [['hotel', 'amenity']]
        verbose_name = _('Hotel Amenity')
        verbose_name_plural = _('Hotel Amenities')
    
    def __str__(self):
        return f"{self.hotel.name} - {self.amenity.name}"


#---------------------- Room Type -----------------------------

class RoomType(models.Model):
    """Types of rooms available in hotel"""

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField( max_length=100, help_text="e.g., Deluxe Room, Suite, Standard Room" )

    slug = models.SlugField(max_length=150)
    description = models.TextField()
    
    # Capacity
    max_adults = models.PositiveIntegerField( default=2, validators=[MinValueValidator(1)] )
    max_children = models.PositiveIntegerField(default=2)
    max_occupancy = models.PositiveIntegerField( default=3, help_text="Total maximum occupancy (adults + children)" )
    
    # Room Details
    number_of_beds = models.PositiveIntegerField(default=1)
    
    BED_TYPE_CHOICES = [
        ('single', 'Single Bed'),
        ('double', 'Double Bed'),
        ('queen', 'Queen Bed'),
        ('king', 'King Bed'),
        ('twin', 'Twin Beds'),
    ]
    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES, default='double')
        
    # Pricing
    base_price = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text="Base price per night" )

    weekend_price = models.DecimalField( max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weekend pricing (if different)" )

    extra_adult_charge = models.DecimalField( max_digits=8, decimal_places=2, default=Decimal('0.00'), help_text="Additional charge per extra adult" )

    extra_child_charge = models.DecimalField( max_digits=8, decimal_places=2, default=Decimal('0.00'), help_text="Additional charge per extra child" )
    
    # Meal Plans
    breakfast_included = models.BooleanField(default=False)
    lunch_included = models.BooleanField(default=False)
    dinner_included = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    total_rooms = models.PositiveIntegerField(
        default=0,
        help_text="Total number of this room type"
    )
    
    class Meta:
        ordering = ['hotel', 'base_price']
        verbose_name = _('Room Type')
        verbose_name_plural = _('Room Types')
        unique_together = [['hotel', 'slug']]
        indexes = [
            models.Index(fields=['hotel', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

# --------------------- Room Type Images ----------------------

class RoomTypeImage(models.Model):
    """Images for room types"""
   
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_types_media/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['room_type', 'display_order']
        verbose_name = _('Room Type Image')
        verbose_name_plural = _('Room Type Images')
    
    def __str__(self):
        return f"{self.room_type.name} - Image {self.display_order}"


# -------------------- Room Type Amenities --------------------------

class RoomAmenity(models.Model):
    """Amenities specific to room types"""
   
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    
    CATEGORY_CHOICES = [
        ('bathroom', 'Bathroom'),
        ('bedroom', 'Bedroom'),
        ('entertainment', 'Entertainment'),
        ('food_drink', 'Food & Drink'),
        ('comfort', 'Comfort'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name = _('Room Amenity')
        verbose_name_plural = _('Room Amenities')
    
    def __str__(self):
        return self.name

class RoomTypeAmenity(models.Model):
    """Junction for room type amenities"""
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='room_amenities')
    amenity = models.ForeignKey(RoomAmenity, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = [['room_type', 'amenity']]
    
    def __str__(self):
        return f"{self.room_type.name} - {self.amenity.name}"


# ------------------ Room Inventory --------------------

class Room(models.Model):
    """Individual room instances"""
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=5, help_text="e.g., 101, 201A")
    floor = models.PositiveIntegerField()
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('blocked', 'Blocked'),
    ]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='available',db_index=True)    
    is_smoking_allowed = models.BooleanField(default=False)

    
    class Meta:
        ordering = ['room_type', 'floor', 'room_number']
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        unique_together = [['room_type', 'room_number']]
        indexes = [
                    models.Index(fields=['room_type', 'status']),
                ]
    
    def __str__(self):
        return f"{self.room_type.hotel.name} - Room {self.room_number}"


#----------------------- Room Availability & Pricing (Daily) -------------------------

class RoomAvailability(models.Model):
    """Daily availability and pricing for room types"""
    room_type = models.ForeignKey( RoomType, on_delete=models.CASCADE, related_name='availability' )

    date = models.DateField(db_index=True)
    
    # Availability
    available_rooms = models.PositiveIntegerField(default=0)
    blocked_rooms = models.PositiveIntegerField(default=0)
    
    # Dynamic Pricing
    price_per_night = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))] )

    weekend_surcharge = models.DecimalField( max_digits=8, decimal_places=2, default=Decimal('0.00') )
    seasonal_surcharge = models.DecimalField( max_digits=8, decimal_places=2, default=Decimal('0.00') )

    discount_percentage = models.DecimalField( max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(0), MaxValueValidator(100)] )
    
    # Taxes
    tax_percentage = models.DecimalField( max_digits=5, decimal_places=2,default=Decimal('12.00'),   help_text="GST or tax percentage")
    
    is_available = models.BooleanField(default=True, db_index=True)
    min_stay_nights = models.PositiveIntegerField(default=1,help_text="Minimum nights required for booking")
    
    class Meta:
        ordering = ['room_type', 'date']
        verbose_name = _('Room Availability')
        verbose_name_plural = _('Room Availabilities')
        unique_together = [['room_type', 'date']]
        indexes = [
            models.Index(fields=['room_type', 'date', 'is_available']),
            models.Index(fields=['date', 'is_available']),
        ]
    
    @property
    def final_price(self):
        """Calculate final price after all charges and discounts"""
        base = self.price_per_night + self.weekend_surcharge + self.seasonal_surcharge
        discounted = base - (base * self.discount_percentage / 100)
        tax = discounted * self.tax_percentage / 100
        return discounted + tax
    
    def __str__(self):
        return f"{self.room_type.name} on {self.date}"



# --------------------- Guest ------------------------


from apps.common.models import User
class Guest(models.Model):
    """Guest information"""
    user = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, blank=True, related_name='guest_profile' )
    
    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50, db_index=True)
    email = models.EmailField(db_index=True)
    phone = models.CharField( max_length=20, validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number')] )
    alternate_phone = models.CharField(max_length=20, blank=True, null=True)
    
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField( max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True )
    nationality = models.CharField(max_length=50, blank=True, null=True)
    
    # ID Proof
    id_proof_type = models.CharField(
        max_length=20,
        choices=[
            ('aadhar', 'Aadhar Card'),
            ('pan', 'PAN Card'),
            ('driving_license', 'Driving License'),
            ('voter_id', 'Voter ID'),
        ],
        blank=True,
        null=True
    )
    id_proof_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Address
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, default='India')
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = _('Guest')
        verbose_name_plural = _('Guests')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# ------------------ Hotel Booking -----------------------

class HotelBooking(models.Model):
    """Main booking record"""
    # Guest Info
    primary_guest = models.ForeignKey( Guest, on_delete=models.CASCADE, related_name='primary_bookings' )
    
    # Hotel & Room
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    
    # Dates
    check_in_date = models.DateField(db_index=True)
    check_out_date = models.DateField(db_index=True)
    total_nights = models.PositiveIntegerField()
    
    # Guest Count
    total_adults = models.PositiveIntegerField(default=1)
    total_children = models.PositiveIntegerField(default=0)
    total_rooms = models.PositiveIntegerField(default=1)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField( max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))] )

    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, default='INR')
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True )
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    
    payment_status = models.CharField( max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', db_index=True )
    
    # Booking Details
    booked_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)
    checked_out_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    
    # Contact
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    
    # Special Requests
    special_requests = models.TextField(blank=True, null=True)
    arrival_time = models.TimeField( null=True, blank=True, help_text="Expected arrival time" )
    
    # Coupon/Promo
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Internal
    internal_notes = models.TextField(blank=True, null=True)
    source = models.CharField( max_length=50, default='website', help_text="Booking source (website, app, phone, walk-in)" )
    
    class Meta:
        ordering = ['-booked_at']
        verbose_name = _('Hotel Booking')
        verbose_name_plural = _('Hotel Bookings')
        indexes = [
            models.Index(fields=['booking_reference']),
            models.Index(fields=['hotel', 'check_in_date']),
            models.Index(fields=['primary_guest', 'status']),
            models.Index(fields=['-booked_at']),
            models.Index(fields=['status', 'payment_status']),
        ]
    
    def __str__(self):
        return f"{self.booking_reference} - {self.hotel.name} ({self.check_in_date})"
    
    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount
    
    @property
    def nights_count(self):
        return (self.check_out_date - self.check_in_date).days


# --------------------- Booking Room Details ---------------------

class BookingRoom(models.Model):
    """Individual rooms in a booking"""
    booking = models.ForeignKey( HotelBooking, on_delete=models.CASCADE, related_name='booking_rooms' )
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room = models.ForeignKey( Room, on_delete=models.SET_NULL, null=True, blank=True, help_text="Assigned room (allocated at check-in)")
    
    # Guest Count for this room
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    # Pricing for this room
    room_price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_room_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    # Meal Plan
    breakfast_included = models.BooleanField(default=False)
    lunch_included = models.BooleanField(default=False)
    dinner_included = models.BooleanField(default=False)
    
    # Preferences
    smoking_preference = models.BooleanField(default=False)
    bed_preference = models.CharField(max_length=50, blank=True, null=True)
    floor_preference = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['booking', 'id']
        verbose_name = _('Booking Room')
        verbose_name_plural = _('Booking Rooms')
    
    def __str__(self):
        return f"{self.booking.booking_reference} - {self.room_type.name}"
