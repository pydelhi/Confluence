from __future__ import unicode_literals

from django.db import models

from registration.models import User

# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (
        ('O', 'ON-HOLD'),
        ('A', 'ACCEPTED'),
        ('P', 'POSTED'),
        ('R', 'REJECTED')
    )

    PLATFORM_CHOICES = (
        ('F', 'FACEBOOK'),
        ('T', 'TWITTER'),
        ('A', 'ALL PLATFORMS')
    )

    text = models.CharField(max_length=160)
    attachment = models.CharField

    posted_by = models.ForeignKey(User, related_name='%(class)s_posted_by')
    approved_by = models.ForeignKey(User, related_name='%(class)s_approved_by')

    created_at = models.DateTimeField()
    approved_at = models.DateTimeField()
    posted_at = models.DateTimeField()
    platforms = models.CharField(max_length=1, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
