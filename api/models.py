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
    name: str = models.CharField(max_length=254)
    description: str = models.CharField(max_length=254, default=None, blank=True)

    REQUIRED_FIELDS: List[str] = ['name', 'description']

    def __str__(self) -> str:
        return f"{self.name} - {self.description}"

class User(AbstractUser):
    id: int = models.AutoField(primary_key=True)
    profile_image: Any = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg', blank=True)
    first_name: str = models.CharField(max_length=254)
    last_name: str = models.CharField(max_length=254)
    email: str = models.EmailField(max_length=254)
    date_of_birth: Any = models.DateField()
    password: str = models.CharField(max_length=254, validators=[MinLengthValidator(8)])
    hobbies: Any = models.ManyToManyField(Hobbies, default=None, blank=True)
    friends: Any = models.ManyToManyField('self', default=None, blank=True)
    pending_requests: Any = models.ManyToManyField('self', default=None, blank=True, symmetrical=False, related_name='incoming_requests')
    sent_requests: Any = models.ManyToManyField('self', default=None, blank=True, symmetrical=False, related_name='outgoing_requests')

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'date_of_birth', 'password']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.email}"