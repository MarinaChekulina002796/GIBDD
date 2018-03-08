from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from gibdd_app.models import MedicalCertificate

# форма для авторизации


class AuthorizationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин пользователя:')
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль пользователя:')

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('Пользователь неактивен')
        else:
            raise forms.ValidationError('Неверный логин или пароль')


