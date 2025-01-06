from typing import Any, List
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
class PageView(models.Model):
    count: int = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Page view count: {self.count}"

class Hobbies(models.Model):
    id: int = models.AutoField(primary_key=True)
    name: str = models.CharField(max_length=254, unique=True)
    description: str = models.CharField(max_length=254, default=None, blank=True)

    REQUIRED_FIELDS: List[str] = ['name', 'description']

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} - {self.description}"

class User(AbstractUser):
    id: int = models.AutoField(primary_key=True)
    profile_image: Any = models.ImageField(upload_to='static/api/spa/assets/', default='static/api/spa/assets/default.jpg', blank=True)
    first_name: str = models.CharField(max_length=254)
    last_name: str = models.CharField(max_length=254)
    email: str = models.EmailField(max_length=254, unique=True)
    date_of_birth: Any = models.DateField()
    password: str = models.CharField(max_length=254, validators=[MinLengthValidator(8)])
    hobbies: Any = models.ManyToManyField(Hobbies, default=None, blank=True)
    friends = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='friend_list'
    )    
    pending_requests: Any = models.ManyToManyField('self', default=None, blank=True, symmetrical=False, related_name='incoming_requests')
    sent_requests = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='received_requests'
    )
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'date_of_birth', 'password']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.email}"
    def age(self):
        from datetime import date
        if self.date_of_birth:
            return date.today().year - self.date_of_birth.year
        return None
