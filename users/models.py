from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=15, null=False, blank=False, unique=True)
    is_moderator = models.BooleanField(default=False)
