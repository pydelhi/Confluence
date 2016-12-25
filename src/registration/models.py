from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    TSHIRT_SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tshirt_size = models.CharField(max_length=1, choices=TSHIRT_SIZE_CHOICES)
    contact = models.CharField(max_length=10)
    ticket_id = models.CharField(max_length=30)
