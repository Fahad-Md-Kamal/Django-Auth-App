import os
import uuid
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db import models
from django.urls import reverse

from .managers import CustomAccountManager

def photo_path(instance, filename):
    """
    Modify Profile Image name and store it to desired folder
    """
    _, file_extension = os.path.splitext(filename)
    uid = str(uuid.uuid4()).split('-')[-1]
    return f'profile/{instance.pk}/{uid}{file_extension}'


class UserBase(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model for authenticating & Authentication
    """
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True, default='')
    profile_image = models.ImageField(upload_to=photo_path, default='default-profile.png')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'Auth User'
        verbose_name_plural = 'Auth Users'
        ordering=['-timestamp']
    
    def __str__(self) -> str:
        return f'{self.email}'
    
    def get_absolute_url(self):
        return reverse('user_auth_app:profile_view', args=[self.pk])
