import datetime
from django import forms
from datetime import date
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.urls import reverse_lazy
from datetime import timedelta
from dateutil.relativedelta import *

from gibdd_app.models import MedicalCertificate, License, Category, Driver, LicenseDisqualification, Lisense_Category, \
    AccidentReport, Witness, Lisense_Accident, Inspector, Fine, Car, RegistrationCertificate, Owner, Stealing, Decree, \
    Camera, AutoSchool, CarHistory, DiagnosticCard, Insurance, InsuranceLicense, Accident_Car


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

    def clean_driver_birth(self):
        data = self.cleaned_data['medical_date']
        medical_date_delta = timezone.now()
        if data > medical_date_delta:
            raise forms.ValidationError("Справка не может быть выдана будущим числомы")
        else:
            return data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        exclude = ('date_end_dr_license',)


# class MonthDateYearOrYearField(forms.DateField):
#     def clean(self, value):
#         date_length = len(value)
#
#         if date_length == 4:  # 2003
#             raise forms.ValidationError('Дата должна быть в формате "мм-дд-гггг"')
#         elif 8 <= date_length <= 10:  # 5/10/2003, 05/10/2003, 5/9/2009
#             pass
#         else:
#             raise forms.ValidationError('Дата должна быть в формате "мм-дд-гггг"')
#
#         return super(MonthDateYearOrYearField, self).clean(value)

from django.utils import timezone


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ()

    # проверка на водителя на 18 лет

    def clean_driver_birth(self):
        data = self.cleaned_data['driver_birth']
        birth_date_delta = timezone.now() - relativedelta(years=18)
        birth_date_old = timezone.now() - relativedelta(years=100)
        if data > birth_date_delta:
            raise forms.ValidationError("Водитель не может быть младше 18 лет")
        # elif data > timezone.now():
        #     raise forms.ValidationError("Водитель еще не родился")
        elif data < birth_date_old:
            raise forms.ValidationError("Водитель не может быть старше 100 лет")
        else:
            return data


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


class DiagnosticCardForm(forms.ModelForm):
    class Meta:
        model = DiagnosticCard
        exclude = ()


class HistoryForm(forms.ModelForm):
    class Meta:
        model = CarHistory
        exclude = ()


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        exclude = ()


class InsuranceLicenseForm(forms.ModelForm):
    class Meta:
        model = InsuranceLicense
        exclude = ()


class Accident_CarForm(forms.ModelForm):
    class Meta:
        model = Accident_Car
        exclude = ()
