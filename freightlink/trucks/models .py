# trucks/models.py
from django.db import models
from accounts.models import User

class Truck(models.Model):
    TRUCK_TYPE_CHOICES = (
        ('pickup', 'Pickup'),
        ('canter', 'Canter'),
        ('lorry', 'Lorry'),
        ('semi_trailer', 'Semi-Trailer'),
        ('trailer', 'Trailer'),
    )
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trucks')
    license_plate = models.CharField(max_length=20, unique=True)
    truck_type = models.CharField(max_length=20, choices=TRUCK_TYPE_CHOICES)
    capacity_volume = models.DecimalField(max_digits=10, decimal_places=2, help_text='Capacity in cubic meters')
    capacity_weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='Capacity in tons')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.license_plate} - {self.truck_type}"

class TruckPhoto(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='truck_photos/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.truck.license_plate}"
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']

class TruckDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('license', 'Vehicle License'),
        ('insurance', 'Insurance'),
        ('roadworthy', 'Roadworthy Certificate'),
        ('other', 'Other Document'),
    )
    
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document = models.FileField(upload_to='verification_docs/')
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.document_type} for {self.truck.license_plate}"


# routes/models.py
from django.db import models
from django.utils import timezone
from trucks.models import Truck

class Route(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='routes')
    origin_name = models.CharField(max_length=255)
    origin_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    origin_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_name = models.CharField(max_length=255)
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    estimated_arrival_date = models.DateField()
    estimated_arrival_time = models.TimeField()
    available_capacity_volume = models.DecimalField(max_digits=10, decimal_places=2, help_text='Available volume in cubic meters')
    available_capacity_weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='Available weight in tons')
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price per kilometer in KES')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.origin_name} to {self.destination_name} on {self.departure_date}"
    
    @property
    def is_past_due(self):
        return timezone.now().date() > self.departure_date
    
    @property
    def has_departed(self):
        today = timezone.now().date()
        now = timezone.now().time()
        return (today > self.departure_date) or (today == self.departure_date and now > self.departure_time)
    
    class Meta:
        ordering = ['departure_date', 'departure_time']


# cargo/models.py
from django.db import models
from accounts.models import User

class CargoListing(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('booked', 'Booked'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    CARGO_TYPE_CHOICES = (
        ('general', 'General Goods'),
        ('fragile', 'Fragile Items'),
        ('perishable', 'Perishable Goods'),
        ('electronics', 'Electronics'),
        ('furniture', 'Furniture'),
        ('documents', 'Documents'),
        ('construction', 'Construction Materials'),
        ('other', 'Other'),
    )
    
    business = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cargo_listings')
    cargo_type = models.CharField(max_length=20, choices=CARGO_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='Weight in tons')
    volume = models.DecimalField(max_digits=10, decimal_places=2, help_text='Volume in cubic meters')
    origin_name = models.CharField(max_length=255)
    origin_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    origin_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_name = models.CharField(max_length=255)
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_date_from = models.DateField()
    pickup_date_to = models.DateField()
    delivery_date_from = models.DateField()
    delivery_date_to = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Maximum budget in KES')
    special_requirements = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.origin_name} to {self.destination_name}"
    
    class Meta:
        ordering = ['-created_at']

class CargoPhoto(models.Model):
    cargo = models.ForeignKey(CargoListing, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='cargo_photos/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.cargo.title}"
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']


# bookings/models.py
from django.db import models
from accounts.models import User
from cargo.models import CargoListing
from routes.models import Route

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    cargo_listing = models.ForeignKey(CargoListing, on_delete=models.CASCADE, related_name='bookings')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='bookings')
    business = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_bookings')
    truck_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='truck_owner_bookings')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Agreed price in KES')
    pickup_date = models.DateField()
    pickup_time = models.TimeField()
    estimated_delivery_date = models.DateField()
    estimated_delivery_time = models.TimeField()
    actual_delivery_date = models.DateField(blank=True, null=True)
    actual_delivery_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.cargo_listing.title}"
    
    class Meta:
        ordering = ['-created_at']

class BookingStatusUpdate(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20, choices=Booking.STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_updates')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Status update for Booking #{self.booking.id}: {self.status}"
    
    class Meta:
        ordering = ['-created_at']


# payments/models.py
from django.db import models
from bookings.models import Booking
from accounts.models import User

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_TYPE_CHOICES = (
        ('booking', 'Booking Payment'),
        ('deposit', 'Deposit'),
        ('balance', 'Balance Payment'),
        ('refund', 'Refund'),
    )
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment of KES {self.amount} for Booking #{self.booking.id}"
    
    class Meta:
        ordering = ['-created_at']

class MpesaCallback(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='mpesa_callbacks', null=True, blank=True)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.CharField(max_length=20)
    result_desc = models.CharField(max_length=255)
    mpesa_receipt_number = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    raw_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"M-Pesa Callback - {self.mpesa_receipt_number or self.checkout_request_id}"
    
    class Meta:
        ordering = ['-created_at']


# matching/models.py
from django.db import models
from cargo.models import CargoListing
from routes.models import Route

class RouteMatch(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    )
    
    cargo = models.ForeignKey(CargoListing, on_delete=models.CASCADE, related_name='route_matches')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='cargo_matches')
    match_score = models.DecimalField(max_digits=5, decimal_places=2, help_text='Score from 0-100')
    price_estimate = models.DecimalField(max_digits=10, decimal_places=2)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_deviation_km = models.DecimalField(max_digits=10, decimal_places=2, help_text='Deviation from route for pickup')
    delivery_deviation_km = models.DecimalField(max_digits=10, decimal_places=2, help_text='Deviation from route for delivery')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Match: {self.cargo.title} with route {self.route.id} (Score: {self.match_score})"
    
    class Meta:
        ordering = ['-match_score']


# notifications/models.py
from django.db import models
from accounts.models import User

class Notification(models.Model):
    TYPE_CHOICES = (
        ('booking_request', 'Booking Request'),
        ('booking_update', 'Booking Status Update'),
        ('payment', 'Payment Notification'),
        ('route_match', 'Route Match'),
        ('system', 'System Notification'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    related_object_type = models.CharField(max_length=50, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.notification_type}: {self.title} for {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']


# reviews/models.py
from django.db import models
from accounts.models import User
from bookings.models import Booking

class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(help_text='Rating from 1-5')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username} - {self.rating}/5"
    
    class Meta:
        ordering = ['-created_at']
        # Ensure one review per user per booking
        unique_together = ('booking', 'reviewer')


# api/models.py
from django.db import models
from accounts.models import User
import uuid
import secrets

class APIKey(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('revoked', 'Revoked'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    key_name = models.CharField(max_length=100)
    key_prefix = models.CharField(max_length=10, unique=True)
    key_hash = models.CharField(max_length=255)  # Stored securely hashed, not plaintext
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_used = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"API Key: {self.key_name} ({self.key_prefix}...)"
    
    @classmethod
    def generate_key(cls):
        # Generate a secure API key
        prefix = uuid.uuid4().hex[:8]
        key = secrets.token_urlsafe(32)
        return f"{prefix}.{key}", prefix
    
    class Meta:
        ordering = ['-created_at']