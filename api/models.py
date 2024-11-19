from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class Hobbies(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.description}"

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=30)
    hobbies = models.ManyToManyField(Hobbies, default=None)
    friends = models.ManyToManyField('self', default=None)
    pending_requests = models.ManyToManyField('self', default=None)
    sent_requests = models.ManyToManyField('self', default=None)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'date_of_birth', 'password']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"