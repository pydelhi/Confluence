from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models

from confluence.settings import TICKET_PALTFORM_CHOICES

# Create your models here.


class User(AbstractUser):
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

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tshirt_size = models.CharField(max_length=1, choices=TSHIRT_SIZE_CHOICES)
    contact = models.CharField(max_length=10)
    ticket_id = models.CharField(max_length=30)
    ticketing_platform = models.CharField(max_length=1,
                                          choices=TICKET_PALTFORM_CHOICES,
                                          default=TICKET_PALTFORM_CHOICES[0])

    def __str__(self):
        return "Name: " + self.first_name + " Ticketing Platform: " + \
               self.ticketing_platform + " Ticket ID: " + self.ticket_id


class UserAttendance(models.Model):
    user = models.ForeignKey(User)
    attended_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " Attended On: " + str(self.attended_on)
