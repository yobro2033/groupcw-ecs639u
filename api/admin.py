from django.contrib import admin

# Register your models here.

from .models import Hobbies, User

admin.site.register(Hobbies)
admin.site.register(User)