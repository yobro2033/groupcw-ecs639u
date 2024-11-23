from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Hobbies


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'hobbies',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Enter date of birth'}
            ),
            'hobbies': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'profile_image',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'hobbies',
            'friends',
            'pending_requests',
            'sent_requests',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Enter date of birth'}
            ),
            'hobbies': forms.CheckboxSelectMultiple(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class PasswordEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
        }

class HobbiesForm(forms.ModelForm):
    class Meta:
        model = Hobbies
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hobby name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hobby description'}),
        }

    def save(self, commit=True):
        hobby = super().save(commit=False)
        if commit:
            hobby.save()
        return hobby

