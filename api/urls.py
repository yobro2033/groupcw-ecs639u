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
from django.urls import include, path, re_path
from django.http import HttpResponse

from . import views

urlpatterns = [

    path('', views.home,name='home'),

    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='signup'),

    path('api/logout/', views.logout, name='logout'),

    path('api/hobbies/', views.get_hobbies, name='get_hobbies'),
    path('api/hobbies/add/', views.create_new_hobby, name='create_new_hobby'),

    path('api/match_users_by_hobbies/', views.match_users_by_hobbies, name='match_users_by_hobbies'),
    path('api/user/<int:user_id>/', views.get_user_profile, name='get_user_profile'),
    path('api/my_profile', views.get_my_profile, name='get_my_profile'),

    path('api/users/', views.search_users, name='search_users'),

    path('api/friends/', views.get_friends, name='get_friends'),
    path('api/friend_requests/', views.get_friend_requests, name='get_friend_requests'),
    path('api/sent_requests/', views.get_sent_requests, name='get_sent_requests'),
    path('api/friend_request/send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('api/friend_request/accept/<int:user_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('api/friend_request/reject/<int:user_id>/', views.reject_friend_request, name='reject_friend_request'),

    path('api/friend/remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('api/sent_request/remove/<int:user_id>/', views.remove_sent_request, name='remove_sent_request'),
    path('api/received_request/remove/<int:user_id>/', views.remove_received_request, name='remove_received_request'),

    path('api/profile/update/', views.update_profile, name='update_profile'),
    path('api/profile/change_password/', views.change_password, name='change_password'),

    # do re_path to catch all other urls apart from anything start with /admin
    re_path(r'^(?!admin).*$', views.catchall_not_found, name='catchall'),
]
