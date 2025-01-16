import json
import sys
from typing import List, Dict, Any, Union

from functools import wraps
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view as require_http_methods
from .models import User, Hobbies
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils.timezone import datetime
from .forms import UserCreateForm, UserEditForm, PasswordEditForm, HobbiesForm, AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
class Hobby:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description
        }

def login_required_or_read_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return view_func(request, *args, **kwargs)
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=401)
    return _wrapped_view

def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def catchall_not_found(request : HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index_404.html', {})

def process_common_hobbies(request: HttpRequest, other_users: List[User], current_user_hobbies: set) -> JsonResponse:
    try:
        user_matches = []
        for user in other_users:
            user_hobbies = set(user.hobbies.values_list('id', flat=True))
            common_hobbies = current_user_hobbies.intersection(user_hobbies)
            isFriend = user in request.user.friends.all()
            hasPendingRequest = user in request.user.pending_requests.all()
            hasSentRequest = user in request.user.sent_requests.all()
            user_matches.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_image': user.profile_image.url,
                'common_hobby_count': len(common_hobbies),
                'hobbies': list(user.hobbies.values('id', 'name')),
                'isFriend': isFriend,
                'hasPendingRequest': hasPendingRequest,
                'hasSentRequest': hasSentRequest,
            })

        user_matches.sort(key=lambda x: (-x['common_hobby_count'], x['first_name']))

        page = request.GET.get('page', 1)
        paginator = Paginator(user_matches, 10)

        try:
            paginated_users = paginator.page(page)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        response_data = {
            'total_pages': paginator.num_pages,
            'current_page': paginated_users.number,
            'users': list(paginated_users),
        }

        return JsonResponse({'result': response_data, 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ process_common_hobbies: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

def update_profile_image(request: HttpRequest) -> JsonResponse:
    try:
        if request.method == 'GET':
            # Get all users and update the path with static/api/spa/assets/default.jpg
            users = User.objects.all()
            number_updated = 0
            for user in users:
                try:
                    user.profile_image = 'static/api/spa/assets/default.jpg'
                    user.save()
                    number_updated += 1
                except Exception as e:
                    print(f'[ERROR] @ update_profile_image: {user.id} - {user.first_name} {user.last_name}')
                    print(f'[ERROR] @ update_profile_image: {e}')
            return JsonResponse({'result': f'Updated {number_updated} users', 'success': 'true'}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
    except Exception as e:
        print('[ERROR] @ update_profile_image: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET", "POST"])
@csrf_protect
def login(request: HttpRequest) -> HttpResponse:
    try:
        form = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')
            else:
                return render(request, 'registration/login.html', {'form': form})
        else:
            return render(request, 'registration/login.html', {'form': form})
    except Exception as e:
        print('[ERROR] @ login: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return render(request, 'registration/login.html', {'form': form})

@require_http_methods(["GET", "POST"])
@csrf_protect
def sign_up(request: HttpRequest) -> HttpResponse:
    try:
        if request.method == 'POST':
            data_form = request.POST
            # add username to form
            email = data_form['email']
            data_form = data_form.copy()
            data_form['username'] = email
            form = UserCreateForm(data_form)
            
            if data_form["password1"] != data_form["password2"]:
                form.add_error('password1', 'Passwords do not match')
                form.add_error('password2', 'Passwords do not match')
                return render(request, 'registration/signup.html', {'form': form})
            
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email is already in use')
                return render(request, 'registration/signup.html', {'form': form})
            
            if (datetime.now().year - int(request.POST['date_of_birth'].split("-")[0])) < 12:
                form.add_error('date_of_birth', 'You must be at least 12 years old to sign up')
                return render(request, 'registration/signup.html', {'form': form})
            
            if form.is_valid():
                try:
                    new_user = form.save()
                    hobbies = request.POST.getlist('hobbies')
                    new_user.hobbies.set(hobbies)
                    user = authenticate(username=data_form["username"], password=data_form["password1"])
                    auth_login(request, user)
                    return redirect('home')
                except IntegrityError as e:
                    print(f"IntegrityError: {e}")
                    form.add_error('username', 'Username already exists')
                    return render(request, 'registration/signup.html', {'form': form})
            else:
                print(f"Incorrect form: {form.errors}")
                return render(request, 'registration/signup.html', {'form': form})
        else:
            form = UserCreateForm()
            return render(request, 'registration/signup.html', {'form': form})
    except Exception as e:
        print('[ERROR] @ sign_up: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return render(request, 'registration/signup.html', {'form': form})

@require_http_methods(["GET"])
@login_required_or_read_only
def get_hobbies(request: HttpRequest) -> JsonResponse:
    try:
        if request.method == 'GET':
            hobbies = Hobbies.objects.all()
            hobbies_list = list(hobbies.values('id', 'name'))
            return JsonResponse({'result': hobbies_list, 'success': 'true'}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
    except Exception as e:
        print('[ERROR] @ get_hobbies: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET"])
@login_required
def match_users_by_hobbies(request: HttpRequest) -> JsonResponse:
    try:
        if request.method == 'GET':
            current_user = request.user
            current_user_hobbies = set(current_user.hobbies.values_list('id', flat=True))
            other_users = User.objects.exclude(id=current_user.id).prefetch_related('hobbies')
            return process_common_hobbies(request, other_users, current_user_hobbies)
        else:
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
    except Exception as e:
        print('[ERROR] @ match_users_by_hobbies: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET"])
@login_required
def get_user_profile(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        if request.method == 'GET':
            user = get_object_or_404(User, id=user_id)
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'profile_image': user.profile_image.url,
                'hobbies': list(user.hobbies.values('id', 'name'))
            }
            return JsonResponse({'result': user_data, 'success': 'true'}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
    except Exception as e:
        print('[ERROR] @ get_user_profile: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET"])
@login_required
def get_my_profile(request: HttpRequest) -> JsonResponse:
    try:
        if request.method == 'GET':
            user = request.user
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'date_of_birth': user.date_of_birth,
                'profile_image': user.profile_image.url,
                'hobbies': list(user.hobbies.values('id', 'name'))
            }
            return JsonResponse({'result': user_data, 'success': 'true'}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
    except Exception as e:
        print('[ERROR] @ get_my_profile: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["POST"])
@csrf_protect
@login_required
def send_friend_request(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friend = get_object_or_404(User, id=user_id)

            if friend in current_user.friends.all():
                return JsonResponse({'error': 'User is already your friend', 'success': 'false'}, status=400)

            if friend in current_user.sent_requests.all():
                return JsonResponse({'error': 'Friend request already sent', 'success': 'false'}, status=400)

            if friend in current_user.pending_requests.all():
                return JsonResponse({'error': 'Friend request already received', 'success': 'false'}, status=400)
            
            current_user.sent_requests.add(friend)
            friend.pending_requests.add(current_user)

            return JsonResponse({'result': 'Friend request sent', 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ send_friend_request: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["POST"])
@csrf_protect
@login_required
def accept_friend_request(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friend = get_object_or_404(User, id=user_id)

            if friend not in current_user.pending_requests.all():
                return JsonResponse({'error': 'No friend request from this user', 'success': 'false'}, status=400)

            current_user.pending_requests.remove(friend)
            current_user.friends.add(friend)
            friend.friends.add(current_user)

            return JsonResponse({'result': 'Friend request accepted', 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ accept_friend_request: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["POST"])
@csrf_protect
@login_required
def reject_friend_request(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friend = get_object_or_404(User, id=user_id)

            if friend not in current_user.pending_requests.all():
                return JsonResponse({'error': 'No friend request from this user', 'success': 'false'}, status=400)

            current_user.pending_requests.remove(friend)
            friend.sent_requests.remove(current_user)

            return JsonResponse({'result': 'Friend request rejected', 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ reject_friend_request: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET"])
@login_required
def get_friends(request: HttpRequest) -> JsonResponse:
    try:
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friends = current_user.friends.all()
            friend_list = [
                {
                    'id': friend.id,
                    'first_name': friend.first_name,
                    'last_name': friend.last_name,
                    'profile_image': friend.profile_image.url,
                }
                for friend in friends
            ]
            return JsonResponse({'result': friend_list, 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ get_friends: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET"])
@login_required
def get_friend_requests(request: HttpRequest) -> JsonResponse:
    try:
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friend_requests = current_user.pending_requests.all()
            friend_request_list = [
                {
                    'id': friend.id,
                    'first_name': friend.first_name,
                    'last_name': friend.last_name,
                    'profile_image': friend.profile_image.url,
                }
                for friend in friend_requests
            ]
            return JsonResponse({'result': friend_request_list, 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ get_friend_requests: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET"])
@login_required
def get_sent_requests(request: HttpRequest) -> JsonResponse:
    try:
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            sent_requests = current_user.sent_requests.all()
            sent_request_list = [
                {
                    'id': friend.id,
                    'first_name': friend.first_name,
                    'last_name': friend.last_name,
                    'profile_image': friend.profile_image.url,
                }
                for friend in sent_requests
            ]
            return JsonResponse({'result': sent_request_list, 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ get_sent_requests: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["DELETE"])
@login_required
def remove_friend(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        if request.method != 'DELETE':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friend = get_object_or_404(User, id=user_id)

            if friend not in current_user.friends.all():
                return JsonResponse({'error': 'User is not your friend', 'success': 'false'}, status=400)

            current_user.friends.remove(friend)
            friend.friends.remove(current_user)

            return JsonResponse({'result': 'Friend removed', 'success': 'true'}, status=204)
    except Exception as e:
        print('[ERROR] @ remove_friend: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["DELETE"])
@login_required
def remove_sent_request(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        if request.method != 'DELETE':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friend = get_object_or_404(User, id=user_id)

            if friend not in current_user.sent_requests.all():
                return JsonResponse({'error': 'No friend request sent to this user', 'success': 'false'}, status=400)

            current_user.sent_requests.remove(friend)
            friend.pending_requests.remove(current_user)

            return JsonResponse({'result': 'Sent request removed', 'success': 'true'}, status=204)
    except Exception as e:
        print('[ERROR] @ remove_sent_request: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["DELETE"])
@login_required
def remove_received_request(request: HttpRequest, user_id: int) -> JsonResponse:
    try:
        if request.method != 'DELETE':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            friend = get_object_or_404(User, id=user_id)

            if friend not in current_user.pending_requests.all():
                return JsonResponse({'error': 'No friend request received from this user', 'success': 'false'}, status=400)

            current_user.pending_requests.remove(friend)
            friend.sent_requests.remove(current_user)

            return JsonResponse({'result': 'Received request removed', 'success': 'true'}, status=204)
    except Exception as e:
        print('[ERROR] @ remove_received_request: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["PUT"])
@login_required
def update_profile(request: HttpRequest) -> JsonResponse:
    try:
        if request.method != 'PUT':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            data = request.data

            current_user.username = data.get('email', current_user.email)
            current_user.first_name = data.get('first_name', current_user.first_name)
            current_user.last_name = data.get('last_name', current_user.last_name)
            current_user.email = data.get('email', current_user.email)
            current_user.date_of_birth = data.get('date_of_birth', current_user.date_of_birth)

            hobbies = data.get('hobbies', [])
            current_user.hobbies.set(hobbies)

            current_user.save()

            return JsonResponse({'result': 'Profile updated', 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ update_profile: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["POST"])
@csrf_protect
@login_required
def change_password(request: HttpRequest) -> JsonResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            current_user = request.user
            data = request.data
            if data.get('new_password') != data.get('new_password_confirm'):
                return JsonResponse({'error': 'Passwords do not match', 'success': 'false'}, status=400)
            if not current_user.check_password(data.get('old_password')):
                return JsonResponse({'error': 'Incorrect old password', 'success': 'false'}, status=400)
            current_user.set_password(data.get('new_password'))
            current_user.save()
            auth_login(request, current_user)
            return JsonResponse({'result': 'Password changed', 'success': 'true'}, status=200)
    except Exception as e:
        print('[ERROR] @ change_password: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["PUT"])
@login_required
def create_new_hobby(request: HttpRequest) -> JsonResponse:
    try:
        if request.method != 'PUT':
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
        else:
            try:
                data = request.data
                form = HobbiesForm(data)
                if form.is_valid():
                    form.save()
                    hobby = Hobbies.objects.get(name=data['name'])
                    return JsonResponse({'result': {'id': hobby.id, 'name': hobby.name}, 'success': 'true'}, status=201)
                listFormErrors = ""
                for key, value in form.errors.items():
                    for error in value:
                        listFormErrors += f"{key}: {error}\n"
                return JsonResponse({'error': listFormErrors, 'success': 'false'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        print('[ERROR] @ create_new_hobby: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["GET"])
@login_required
def search_users(request: HttpRequest) -> JsonResponse:
    try:
        if request.method == 'GET':
            params = request.GET
            search_kw = params.get('search')
            l_age = params.get('l_age')
            u_age = params.get('u_age')
            users = User.objects.exclude(id=request.user.id)
            current_user = request.user
            current_user_hobbies = set(current_user.hobbies.values_list('id', flat=True))
            if search_kw:
                # filter if first_name, last_name, email contains search_kw, this includes contains part of the string
                if search_kw != '':
                    users = users.filter(first_name__icontains=search_kw) | users.filter(last_name__icontains=search_kw) | users.filter(email__icontains=search_kw)
            if l_age:
                current_year = datetime.now().year
                l_year = current_year - int(l_age)
                users = users.filter(date_of_birth__lte=f'{l_year}-01-01')
            if u_age:
                current_year = datetime.now().year
                u_year = current_year - int(u_age)
                users = users.filter(date_of_birth__gte=f'{u_year}-01-01')
            return process_common_hobbies(request, users, current_user_hobbies)
        else:
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
    except Exception as e:
        print('[ERROR] @ search_users: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)

@require_http_methods(["POST"])
@csrf_protect
@login_required
def logout(request : HttpRequest) -> JsonResponse:
    try:
        if request.method == 'POST':
            headers = request.headers
            auth.logout(request)
            return JsonResponse({'result': 'Successfully logged out', 'success': 'true'}, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed', 'success': 'false'}, status=405)
    except Exception as e:
        print('[ERROR] @ logout: {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return JsonResponse({'error': 'An error occurred', 'success': 'false'}, status=500)