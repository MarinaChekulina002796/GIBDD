from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from gibdd_app.models import MedicalCertificate, License, Category


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


class MedicalCertificateForm(forms.ModelForm):
    class Meta:
        model = MedicalCertificate
        exclude = ()
        success_url = reverse_lazy('main')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()
        success_url = reverse_lazy('main')


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        exclude = ()


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()