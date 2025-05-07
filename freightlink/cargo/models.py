from django.db import models
from accounts.models import  User

class CargoListing(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('booked', 'Booked'),
        ('in_transit', 'In-transit'),
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
    weight = models.DecimalField(max_digits=9, decimal_places=6)
    origin_latitude = models.DecimalField(max_digits=9 , decimal_places=6)
    origin_logitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=9)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_date_from = models.DateField()
    pickup_date_to = models.DateField()
    delivery_date_from = models.DateField()
    delivery_date_to = models.DateField()
    budget = models.DecimalField(max_digits=9 , decimal_places=5 , blank=True, null=True, help_text='maximum budget in KES')
    special_requirements = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} - {self.origin_name} to {self.destination_name}"
    
    class meta:
        oderering = ['-created_at']

class CargoPhoto(models.Model):
    cargo = models.ForeignKey(CargoListing, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='cargo_photos/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.cargo.tite}"
    
    class Meta:
        ordering = ['is_primary', '-uploaded_at']


    




# Create your models here.
