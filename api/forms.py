from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Hobbies

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class UserCreateForm(UserCreationForm):
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobbies.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'date_of_birth',
            'password1',
            'password2',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Enter date of birth'}),
        }

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
        if commit:
            user.save()
        return user

    def cleaned_data(self) -> Any:
        cleaned_data = super().cleaned_data()
        cleaned_data['username'] = cleaned_data['email']
        return cleaned_data

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

    def save(self, commit: bool = True) -> User:
        user: User = super().save(commit=False)
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

    def save(self, commit: bool = True) -> Hobbies:
        hobby: Hobbies = super().save(commit=False)
        if commit:
            hobby.save()
        return hobby