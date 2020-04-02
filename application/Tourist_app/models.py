from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):

    role = models.CharField("Роль", max_length=15, default='student')
    tel = models.CharField("Телефон", max_length=15, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'role', 'tel']

    def __str__(self):
        return self.username


