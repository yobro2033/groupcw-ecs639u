from django.contrib import admin

# Register your models here.

from .models import PageView, Hobbies, User

admin.site.register(admin, User)