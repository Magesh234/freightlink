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
