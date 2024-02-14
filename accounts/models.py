from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    follower = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        symmetrical=False,
        related_name='following'
    )
    profile_picture = models.ImageField(null=True, blank=True)
    profile_banner = models.ImageField(null=True, blank=True)
