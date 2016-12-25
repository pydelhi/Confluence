from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from registration.models import User

# Create your models here.

class Talks(models.Model):
    TALK_CHOICES = (
        ('T', 'TALK'),
        ('D', 'DEV SPRINTS'),
        ('W', 'WORKSHOP')
    )

    CATEGORY_CHOICES = (
        ('B', 'BEGINNER'),
        ('I', 'INTERMEDIATE'),
        ('A', 'ADVANCED')
    )

    talk_name = models.CharField(max_length=100)
    duration = models.FloatField()
    group = models.CharField(max_length=1, choices=TALK_CHOICES)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    speaker = models.ForeignKey(User)

    class Meta:
        verbose_name = _('Talk')
        verbose_name_plural = _('Talks')
