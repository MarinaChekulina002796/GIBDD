import datetime
from django import forms
from datetime import date
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import SelectDateWidget
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.urls import reverse_lazy
from datetime import timedelta
from dateutil.relativedelta import *
from django.utils import timezone
from psycopg2 import extras

from gibdd_app.models import *


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
        widgets = {'medical_date': forms.SelectDateWidget(years=range(2005, 2025)), }
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
        widgets = {'date_open_category': forms.SelectDateWidget(years=range(1940, 2025)), }
        model = Category
        exclude = ()


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        exclude = ('date_end_dr_license',)


class DriverForm(forms.ModelForm):
    class Meta:
        widgets = {'driver_birth': forms.SelectDateWidget(years=range(1940, 2025)), }
        model = Driver
        exclude = ()

    # проверка на водителя на 16 лет

    def clean_driver_birth(self):
        data = self.cleaned_data['driver_birth']
        birth_date_delta = timezone.now() - relativedelta(years=16)
        birth_date_old = timezone.now() - relativedelta(years=100)
        if data > birth_date_delta:
            raise forms.ValidationError("Водитель не может быть младше 16 лет")
        # elif data > timezone.now():
        #     raise forms.ValidationError("Водитель еще не родился")
        elif data < birth_date_old:
            raise forms.ValidationError("Водитель не может быть старше 100 лет")
        else:
            return data


class LicenseDisqualificationForm(forms.ModelForm):
    class Meta:
        widgets = {'disqualif_date_from': forms.SelectDateWidget(years=range(2005, 2035)),
                   'disqualif_date_end': forms.SelectDateWidget(years=range(2005, 2035)), }
        model = LicenseDisqualification
        exclude = ()


class Licen_CatForm(forms.ModelForm):
    class Meta:
        model = Lisense_Category
        exclude = ()


class AccidentReportForm(forms.ModelForm):
    class Meta:
        widgets = {'accident_date': forms.SelectDateWidget(years=range(2016, 2040)),
                   'accident_paper_date': forms.SelectDateWidget(years=range(2016, 2040)),
                   'accident_time': forms.TimeInput(),
                   }
        model = AccidentReport
        exclude = ()


class WitnessForm(forms.ModelForm):
    class Meta:
        widgets = {'witness_email': forms.EmailInput(), }
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
        widgets = {'date_of_payment_fine': forms.SelectDateWidget(years=range(2017, 2020)), }
        model = Fine
        exclude = ()


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ()


class RegistrationCertificateForm(forms.ModelForm):
    class Meta:
        widgets = {'registr_certificate_year': forms.SelectDateWidget(years=range(1960, 2025)), }
        model = RegistrationCertificate
        exclude = ()


class OwnerForm(forms.ModelForm):
    class Meta:
        widgets = {'owner_date_give': forms.SelectDateWidget(years=range(2005, 2025)), }
        model = Owner
        exclude = ()


class StealingForm(forms.ModelForm):
    class Meta:
        widgets = {'stealing_date': forms.SelectDateWidget(years=range(2000, 2025)), }
        model = Stealing
        exclude = ()


class DecreeForm(forms.ModelForm):
    class Meta:
        widgets = {'decree_date': forms.SelectDateWidget(years=range(2010, 2025)), }
        model = Decree
        exclude = ()


class CameraForm(forms.ModelForm):
    class Meta:
        widgets = {'camera_vertification_from': forms.SelectDateWidget(years=range(2015, 2025)),
                   'camera_vertification_to': forms.SelectDateWidget(years=range(2018, 2030)), }
        model = Camera
        exclude = ()


class AutoschoolForm(forms.ModelForm):
    class Meta:
        model = AutoSchool
        exclude = ()


class DiagnosticCardForm(forms.ModelForm):
    class Meta:
        widgets = {'diagnostic_date_from': forms.SelectDateWidget(years=range(2014, 2025)),
                   'diagnostic_date_to': forms.SelectDateWidget(years=range(2015, 2026)), }
        model = DiagnosticCard
        exclude = ()


class HistoryForm(forms.ModelForm):
    class Meta:
        widgets = {'history_birth': forms.SelectDateWidget(years=range(1930, 2025)),
                   'history_date_from': forms.SelectDateWidget(years=range(1990, 2030)),
                   'history_date_to': forms.SelectDateWidget(years=range(1990, 2030)), }
        model = CarHistory
        exclude = ()


class InsuranceForm(forms.ModelForm):
    class Meta:
        widgets = {'insurance_date_from': forms.SelectDateWidget(years=range(2016, 2035)),
                   'insurance_date_to': forms.SelectDateWidget(years=range(2016, 2035)), }
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


class EuroprotocolForm(forms.ModelForm):
    class Meta:
        widgets = {'europrotocol_date': forms.SelectDateWidget(years=range(2016, 2035)),
                   }
        model = Europrotocol
        exclude = ()


class Autoschool_DriverForm(forms.ModelForm):
    class Meta:
        widgets = {'school_date_from': forms.SelectDateWidget(years=range(2016, 2035)),
                   'school_date_to': forms.SelectDateWidget(years=range(2016, 2035)),
                   }
        model = Autoschool_Driver
        exclude = ()
