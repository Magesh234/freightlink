from django.db import models
from accounts.models import User

class Truck(models.Model):
	TRUCK_TYPE_CHOICES = (
		('pickup', 'Pickup'),
		('canter', 'Canter'),
		('lorry', 'Lorry'),
		('semi_trailer', 'Semi_trailer'),
		('trailer', 'Trailer'),
	)

	owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='trucks')
	licence_plate = models.CharField

# Create your models here.


