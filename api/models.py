from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # O'zgaruvchilar va maydonlarni qo'shing
    email=models.EmailField()


    def __str__(self):
        return self.username
        
