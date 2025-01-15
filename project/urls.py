"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from api.views import login_view, register_view


def custom_login_view(request):
    return render(request, 'registration/login.html')

def custom_signup_view(request):
    return render(request, 'registration/signup.html')

urlpatterns = [
    path('', include('api.urls')),
    path('health', lambda request: HttpResponse("OK")),
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('Login/', login_view, name='login'),
    path('Signup/', register_view, name='signup'),
    
   # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('signup/', auth_views.TemplateView.as_view(template_name='registration/signup.html'), name='signup'),
]
