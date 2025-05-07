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