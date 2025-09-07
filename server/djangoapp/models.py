"""
Car Models
----------
This file defines Django ORM models for representing car makes and models

Models:
- CarMake: Represents a car manufacturer/brand
- CarModel: Represents a specific car model linked to a CarMake
"""

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    # Represents a car manufacturer
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        # Return the name as the string representation
        return self.name  

    
class CarModel(models.Model):
    # Represents a specific car model that belongs to a CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Many-to-One relationship
    name = models.CharField(max_length=100)

    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    
    year = models.IntegerField(default=2023,
        validators=[
            MaxValueValidator(2023), # Prevents future years
            MinValueValidator(2015)  # Restricts to modern models
        ])

    def __str__(self):
        # Return the name as the string representation
        return self.name  
    