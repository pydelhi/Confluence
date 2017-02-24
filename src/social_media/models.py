from __future__ import unicode_literals

from django.db import models
from uuid_upload_path import upload_to

from registration.models import User

# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (
        ('H', 'ON-HOLD'),
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
    photo = models.ImageField(upload_to=upload_to, blank=True, null=True)

    created_by = models.ForeignKey(User, related_name='%(class)s_posted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    moderated_by = models.ForeignKey(User, related_name='%(class)s_approved_by', null=True)
    moderated_at = models.DateTimeField(null=True)
    posted_at = models.DateTimeField(null=True)

    platforms = models.CharField(max_length=1, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
