from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('owner', 'Canteen Owner'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Common contact for both roles
    contact = models.CharField(max_length=15, blank=True, null=True)
    
    # Fields specific to canteen owners
    canteen_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
