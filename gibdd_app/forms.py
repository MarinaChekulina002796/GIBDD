from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.urls import reverse_lazy

from gibdd_app.models import MedicalCertificate, License, Category, Driver, LicenseDisqualification, Lisense_Category, \
    AccidentReport, Witness, Lisense_Accident, Inspector, Fine, Car, RegistrationCertificate, Owner, Stealing, Decree, \
    Camera, AutoSchool


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


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        exclude = ()


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ()


class LicenseDisqualificationForm(forms.ModelForm):
    class Meta:
        model = LicenseDisqualification
        exclude = ()


class Licen_CatForm(forms.ModelForm):
    class Meta:
        model = Lisense_Category
        exclude = ()


class AccidentReportForm(forms.ModelForm):
    class Meta:
        model = AccidentReport
        exclude = ()


class WitnessForm(forms.ModelForm):
    class Meta:
        model = Witness
        exclude = ()


class Lisense_AccidentForm(forms.ModelForm):
    class Meta:
        model = Lisense_Accident
        exclude = ()


class InspectorForm(forms.ModelForm):
    class Meta:
        model = Inspector
        exclude = ()


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        exclude = ()


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ()


class RegistrationCertificateForm(forms.ModelForm):
    class Meta:
        model = RegistrationCertificate
        exclude = ()


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        exclude = ()


class StealingForm(forms.ModelForm):
    class Meta:
        model = Stealing
        exclude = ()


class DecreeForm(forms.ModelForm):
    class Meta:
        model = Decree
        exclude = ()


class CameraForm(forms.ModelForm):
    class Meta:
        model = Camera
        exclude = ()


class AutoschoolForm(forms.ModelForm):
    class Meta:
        model = AutoSchool
        exclude = ()