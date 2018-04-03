# Create your views here.
import operator
from functools import reduce

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchVector, SearchRank
from django.db.models import Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls.base import reverse
from django.db.models import Value as V
from dateutil.relativedelta import *
import datetime
from datetime import timedelta
import gibdd_app
from gibdd_app.forms import AuthorizationForm, MedicalCertificateForm, CategoryForm, LicenseForm, DriverForm, \
    LicenseDisqualificationForm, Licen_CatForm, AccidentReportForm, WitnessForm, Lisense_AccidentForm, InspectorForm, \
    FineForm, CarForm, RegistrationCertificateForm, OwnerForm, StealingForm, DecreeForm, CameraForm, AutoschoolForm, \
    HistoryForm, DiagnosticCardForm, InsuranceForm, InsuranceLicenseForm, Accident_CarForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from gibdd_app.models import MedicalCertificate, License, Category, Driver, LicenseDisqualification, Lisense_Category, \
    AccidentReport, Witness, Lisense_Accident, Inspector, Fine, Car, RegistrationCertificate, Owner, Stealing, Decree, \
    Camera, CarHistory, Accident_Car, AutoSchool, DiagnosticCard, Insurance, InsuranceLicense
from django.shortcuts import render


# главная страница ГИБДД
def main(request):
    return render(request, 'gibdd_app/main.html')


def forbidden(request):
    return render(request, 'gibdd_app/forbidden.html')


# список всех справок (по 2 шт в ряд)
@login_required
def med_list(request):
    template = 'gibdd_app/MedicalCertificate_list.html'
    objects_list = MedicalCertificate.objects.all().order_by('medical_number', 'medical_date')

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_list_reg_auto_fine(request):
    template = 'gibdd_app/Mix.html'
    list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
            'fine_amount', 'fine_discount',
            'fine_car_data__car_registr_certificate__registr_certificate_number',
            'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
            'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

    objects_list = Fine.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_list_licen_fine(request):
    template = 'gibdd_app/Mix_licen_fine.html'
    list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
            'fine_amount', 'fine_discount',
            'fine_car_data__car_registr_certificate__registr_certificate_number',
            'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
            'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

    objects_list = Fine.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_list_VIN_stealing(request):
    template = 'gibdd_app/Mix_VIN_stealing.html'
    list = ['pk', 'car_registr_certificate__registr_certificate_VIN',
            'car_registr_certificate__registr_certificate_number',
            'car_registr_certificate__registr_certificate_car_model',
            'car_registr_certificate__registr_certificate_colour',
            'car_owner__owner_surname', 'car_owner__owner_name',
            'car_stealing__stealing_status', 'car_stealing__stealing_date', 'car_stealing__stealing_town']
    objects_list = Car.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_search_VIN_stealing(request):
    template = 'gibdd_app/Mix_VIN_stealing.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'car_registr_certificate__registr_certificate_VIN',
                'car_registr_certificate__registr_certificate_number',
                'car_registr_certificate__registr_certificate_car_model',
                'car_registr_certificate__registr_certificate_colour',
                'car_owner__owner_surname', 'car_owner__owner_name',
                'car_stealing__stealing_status', 'car_stealing__stealing_date', 'car_stealing__stealing_town']

        regs = Car.objects.filter(car_registr_certificate__registr_certificate_VIN__icontains=query).values(*list)

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
    return render(request, template, {'regs': regs, 'query': query})


def mix_list_VIN_history(request):
    template = 'gibdd_app/Mix_VIN_CarHistory.html'
    list = ['pk', 'car_item__car_registr_certificate__registr_certificate_VIN',
            'car_item__car_registr_certificate__registr_certificate_car_model',
            'car_item__car_registr_certificate__registr_certificate_colour',
            'car_item__car_registr_certificate__registr_certificate_year',
            'history_date_from', 'history_date_to', 'history_country', 'history_town'
            ]
    objects_list = CarHistory.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_search_VIN_history(request):
    template = 'gibdd_app/Mix_VIN_CarHistory.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'car_item__car_registr_certificate__registr_certificate_VIN',
                'car_item__car_registr_certificate__registr_certificate_car_model',
                'car_item__car_registr_certificate__registr_certificate_colour',
                'car_item__car_registr_certificate__registr_certificate_year',
                'history_date_from', 'history_date_to', 'history_country', 'history_town'
                ]

        regs = CarHistory.objects.filter(
            car_item__car_registr_certificate__registr_certificate_VIN__icontains=query).values(
            *list)

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
    return render(request, template, {'regs': regs, 'query': query})


def mix_list_VIN_accident(request):
    template = 'gibdd_app/Mix_VIN_Accident.html'
    list = ['pk', 'car__car_registr_certificate__registr_certificate_VIN',
            'car__car_registr_certificate__registr_certificate_number',
            'car__car_registr_certificate__registr_certificate_car_model',
            'car__car_registr_certificate__registr_certificate_colour',
            'accid__accident_date', 'accid__accident_severity'
            ]
    objects_list = Accident_Car.objects.all().values(*list)

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def mix_search_VIN_accident(request):
    template = 'gibdd_app/Mix_VIN_Accident.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'car__car_registr_certificate__registr_certificate_VIN',
                'car__car_registr_certificate__registr_certificate_number',
                'car__car_registr_certificate__registr_certificate_car_model',
                'car__car_registr_certificate__registr_certificate_colour',
                'accid__accident_date', 'accid__accident_severity'
                ]
        regs = Accident_Car.objects.filter(
            car__car_registr_certificate__registr_certificate_VIN__icontains=query).values(
            *list)

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
    return render(request, template, {'regs': regs, 'query': query})


def med_search(request):
    template = 'gibdd_app/MedicalCertificate_list.html'
    query = request.GET.get('q')
    if query:
        meds = MedicalCertificate.objects.filter(Q(medical_number__icontains=query))
    else:
        return HttpResponse('Пожалуйста, заполните строку поиска.')
    return render(request, template, {'meds': meds, 'query': query})


def mix_search(request):
    template = 'gibdd_app/Mix.html'
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    if query1 and query2:
        list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
                'fine_amount', 'fine_discount',
                'fine_car_data__car_registr_certificate__registr_certificate_number',
                'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
                'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

        # regs = Fine.objects.annotate(
        #     search_name=Concat('fine_car_data__car_registr_certificate__registr_certificate_number', V(' '),
        #                        'fine_car_data__car_registr_certificate__registr_certificate_registr_sign'
        #                        )).filter(search_name__icontains=query).values(*list)
        regs = Fine.objects.filter(
            Q(fine_car_data__car_registr_certificate__registr_certificate_number__icontains=query1),
            Q(fine_car_data__car_registr_certificate__registr_certificate_registr_sign__exact=query2)).values(
            *list)
        return render(request, template, {'regs': regs, 'query1': query1, 'query2': query2})

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)


def search_accidents_by_date(request):
    template = 'gibdd_app/Search_accidents_by_date.html'
    query1 = request.GET.get('q')
    query2 = request.GET.get('p')

    list = ['pk', 'car__car_registr_certificate__registr_certificate_VIN',
            'car__car_registr_certificate__registr_certificate_number',
            'car__car_registr_certificate__registr_certificate_car_model',
            'car__car_registr_certificate__registr_certificate_colour',
            'accid__accident_date', 'accid__accident_severity']
    if query1 and query2:
        regs = Accident_Car.objects.all().order_by('accid__accident_date')
        regs = regs.filter(Q(accid__accident_date__range=[query1, query2])).values(*list)
        return render(request, template, {'regs': regs, 'query1': query1, 'query2': query2})
    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
        # regs = Accident_Car.objects.all().order_by('accid__accident_date')
        # regs = regs.filter(Q(accid__accident_date__range=[query1, query2])).values(*list)


def mix_search_licen_fine(request):
    template = 'gibdd_app/Mix_licen_fine.html'
    query = request.GET.get('q')

    if query:
        list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
                'fine_amount', 'fine_discount',
                'fine_car_data__car_registr_certificate__registr_certificate_number',
                'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
                'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']

        regs = Fine.objects.annotate(
            search_name=Concat('fine_license_data__series_dr_license',
                               'fine_license_data__number_dr_license'
                               )).filter(search_name__icontains=query).values(*list)

    else:
        text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
        button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
        tex = (text, button)
        return HttpResponse(tex)
    return render(request, template, {'regs': regs, 'query': query})


# def mix_search_licen_fine(request):
#     template = 'gibdd_app/Mix_licen_fine.html'
#     query1 = request.GET.get('q')
#     query2 = request.GET.get('t')
#
#     if query1 and query2:
#         if query2.exists():
#             list = ['pk', 'fine_decree_data__decree_number', 'fine_status', 'fine_decree_data__decree_date',
#                     'fine_amount', 'fine_discount',
#                     'fine_car_data__car_registr_certificate__registr_certificate_number',
#                     'fine_car_data__car_registr_certificate__registr_certificate_registr_sign',
#                     'fine_license_data__series_dr_license', 'fine_license_data__number_dr_license']
#             criterion1 = Q(fine_license_data__series_dr_license__icontains=query1) & \
#                          Q(fine_license_data__series_dr_license__isnull=False)
#             criterion2 = Q(fine_license_data__number_dr_license__isnull=False) & \
#                          Q(fine_license_data__number_dr_license__icontains=query2)
#
#             regs = Fine.objects.all().filter(criterion1 & criterion2)
#             regs = regs.values(*list)
#             # regs = a.filter(Q(fine_license_data__number_dr_license__icontains=query2)).values(*list)
#
#             # search_name = Concat('fine_license_data__series_dr_license',
#             #                      'fine_license_data__number_dr_license'
#             #                      )).filter(search_name__icontains=query).values(*list)
#         else:
#             text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
#             button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
#             tex = (text, button)
#             return HttpResponse(tex)
#     else:
#         text = '<i><b>Пожалуйста, заполните строку поиска.</b></i> '
#         button = '<ol><button class="btn btn-info" type="button" onclick="history.back()">Назад</button></ol>'
#         tex = (text, button)
#         return HttpResponse(tex)
#     return render(request, template, {'regs': regs, 'query1': query1, 'query2': query2})


@login_required
def categ_list(request):
    template = 'gibdd_app/Category_list.html'
    objects_list = Category.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def license_list(request):
    template = 'gibdd_app/License_list.html'
    objects_list = License.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def driver_list(request):
    template = 'gibdd_app/Driver_list.html'
    objects_list = Driver.objects.all().order_by('driver_surname', 'driver_name', 'driver_patronymic')

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def disq_list(request):
    template = 'gibdd_app/LicenseDisqualification_list.html'
    objects_list = LicenseDisqualification.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


@login_required
def categ_detail(request, pk):
    template = 'gibdd_app/Category_detail.html'

    obj = get_object_or_404(Category, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def med_detail(request, pk):
    template = 'gibdd_app/MedicalCertificate_detail.html'

    obj = get_object_or_404(MedicalCertificate, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def license_detail(request, pk):
    template = 'gibdd_app/License_detail.html'

    obj = get_object_or_404(License, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def driver_detail(request, pk):
    template = 'gibdd_app/Driver_detail.html'

    obj = get_object_or_404(Driver, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def disq_detail(request, pk):
    template = 'gibdd_app/LicenseDisqualification_detail.html'

    obj = get_object_or_404(LicenseDisqualification, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


@login_required
def delete_med(request, pk):
    template = 'gibdd_app/MedicalCertificate_form.html'

    obj = get_object_or_404(MedicalCertificate, pk=pk)
    if request.method == 'POST':
        form = MedicalCertificateForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('med_list'))
    else:
        form = MedicalCertificateForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_categ(request, pk):
    template = 'gibdd_app/Category_form.html'

    obj = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('categ_list'))
    else:
        form = CategoryForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_license(request, pk):
    template = 'gibdd_app/License_form.html'

    obj = get_object_or_404(License, pk=pk)
    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('license_list'))
    else:
        form = LicenseForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_driver(request, pk):
    template = 'gibdd_app/Driver_form.html'

    obj = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('driver_list'))
    else:
        form = DriverForm(instance=obj)

    return render(request, template, {'form': form})


@login_required
def delete_disq(request, pk):
    template = 'gibdd_app/LicenseDisqualification_form.html'

    obj = get_object_or_404(LicenseDisqualification, pk=pk)
    if request.method == 'POST':
        form = LicenseDisqualificationForm(request.POST, request.FILES, instance=obj)
        obj.delete()
        messages.success(request, 'Successful delete')
        return redirect(reverse('disq_list'))
    else:
        form = LicenseDisqualificationForm(instance=obj)

    return render(request, template, {'form': form})


def services(request):
    return render(request, 'gibdd_app/services_for_drivers.html')


def gibdd(request):
    return render(request, 'gibdd_app/gibdd.html')


def participants(request):
    return render(request, 'gibdd_app/participants.html')


@login_required
def workers(request):
    return render(request, 'gibdd_app/workers.html')


def statistics(request):
    return render(request, 'gibdd_app/statistics.html')


def contacts(request):
    return render(request, 'gibdd_app/contacts.html')


# для авторизации уже зарегистрированного пользователя
def login(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user is not None:
                auth_login(request, user)
            return redirect(reverse('main'))
    else:
        form = AuthorizationForm()
    return render(request, 'gibdd_app/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect(reverse('main'))


@login_required
def add_license(request):
    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
        if form.is_valid():
            # licen = form.save(commit=False)
            # licen.driver_data = request.driver_data
            # licen.medical_certificate_data = request.medical_certificate_data
            # licen.status_dr_license = request.status_dr_license
            licen = License(**form.cleaned_data)
            licen.save()
            return reverse('lic_cat_create')
    else:
        form = LicenseForm()
    template = 'gibdd_app/License_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def update_license(request, pk):
    licen = get_object_or_404(License, pk=pk)
    if request.method == 'POST':
        form = LicenseForm(request.POST, request.FILES, instance=licen)
        if form.is_valid():
            form.save()
        return redirect('license_detail', pk)
    else:
        form = LicenseForm(instance=licen)

    template = 'gibdd_app/License_form.html'
    context = {
        'form': form,
        'licen': licen,
    }

    return render(request, template, context)


@login_required
def add_med(request):
    if request.method == 'POST':
        form = MedicalCertificateForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
        if form.is_valid():
            med = MedicalCertificate(**form.cleaned_data)
            med.save()
            return redirect(reverse('license_create'))
    else:
        form = MedicalCertificateForm()

    template = 'gibdd_app/MedicalCertificate_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@permission_required("can_add_lisense_category", login_url='forbidden')
@login_required
def add_lic_cat(request):
    if request.method == 'POST':
        form = Licen_CatForm(request.POST, request.FILES)
        if form.is_valid():
            main_form = Lisense_Category(**form.cleaned_data)
            main_form.save()
            return redirect(reverse('workers'), args=[main_form.pk])
    else:
        form = Licen_CatForm()

    template = 'gibdd_app/Licen_CatForm.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_accident(request):
    if request.method == 'POST':
        form = AccidentReportForm(request.POST, request.FILES)
        if form.is_valid():
            accid = AccidentReport(**form.cleaned_data)
            accid.save()
            return redirect(reverse('workers'), args=[accid.pk])
    else:
        form = AccidentReportForm()

    template = 'gibdd_app/AccidentReport_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_witness(request):
    if request.method == 'POST':
        form = WitnessForm(request.POST, request.FILES)
        if form.is_valid():
            wit = Witness(**form.cleaned_data)
            wit.save()
            return redirect(reverse('workers'), args=[wit.pk])
    else:
        form = WitnessForm()

    template = 'gibdd_app/Witness_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_licen_accid(request):
    if request.method == 'POST':
        form = Lisense_AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            l_a = Lisense_Accident(**form.cleaned_data)
            l_a.save()
            return redirect(reverse('workers'), args=[l_a.pk])
    else:
        form = Lisense_AccidentForm()

    template = 'gibdd_app/Lisense_Accident_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_inspector(request):
    if request.method == 'POST':
        form = InspectorForm(request.POST, request.FILES)
        if form.is_valid():
            insp = Inspector(**form.cleaned_data)
            insp.save()
            return redirect(reverse('workers'), args=[insp.pk])
    else:
        form = InspectorForm()

    template = 'gibdd_app/Inspector_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_fine(request):
    if request.method == 'POST':
        form = FineForm(request.POST, request.FILES)
        if form.is_valid():
            fine = Fine(**form.cleaned_data)
            fine.save()
            return redirect(reverse('workers'), args=[fine.pk])
    else:
        form = FineForm()

    template = 'gibdd_app/Fine_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = Car(**form.cleaned_data)
            car.save()
            return redirect(reverse('workers'), args=[car.pk])
    else:
        form = CarForm()

    template = 'gibdd_app/Car_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_registr(request):
    if request.method == 'POST':
        form = RegistrationCertificateForm(request.POST, request.FILES)
        if form.is_valid():
            reg = RegistrationCertificate(**form.cleaned_data)
            reg.save()
            return redirect(reverse('workers'), args=[reg.pk])
    else:
        form = RegistrationCertificateForm()

    template = 'gibdd_app/RegistrationCertificate_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES)
        if form.is_valid():
            reg = Owner(**form.cleaned_data)
            reg.save()
            return redirect(reverse('workers'), args=[reg.pk])
    else:
        form = OwnerForm()

    template = 'gibdd_app/Owner_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_steal(request):
    if request.method == 'POST':
        form = StealingForm(request.POST, request.FILES)
        if form.is_valid():
            steal = Stealing(**form.cleaned_data)
            steal.save()
            return redirect(reverse('workers'), args=[steal.pk])
    else:
        form = StealingForm()

    template = 'gibdd_app/Stealing_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_decree(request):
    if request.method == 'POST':
        form = DecreeForm(request.POST, request.FILES)
        if form.is_valid():
            decree = Decree(**form.cleaned_data)
            decree.save()
            return redirect(reverse('workers'), args=[decree.pk])
    else:
        form = DecreeForm()

    template = 'gibdd_app/Decree_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_camera(request):
    if request.method == 'POST':
        form = CameraForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Camera(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = CameraForm()

    template = 'gibdd_app/Camera_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_autoschool(request):
    if request.method == 'POST':
        form = AutoschoolForm(request.POST, request.FILES)
        if form.is_valid():
            cam = AutoSchool(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = AutoschoolForm()

    template = 'gibdd_app/AutoSchool_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_history(request):
    if request.method == 'POST':
        form = HistoryForm(request.POST, request.FILES)
        if form.is_valid():
            cam = CarHistory(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = HistoryForm()

    template = 'gibdd_app/History_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_diagnostic_card(request):
    if request.method == 'POST':
        form = DiagnosticCardForm(request.POST, request.FILES)
        if form.is_valid():
            cam = DiagnosticCard(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = DiagnosticCardForm()

    template = 'gibdd_app/DiagnosticCard_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Driver(**form.cleaned_data)
            cam.save()
            return redirect(reverse('license_create'), args=[cam.pk])
    else:
        form = DriverForm()

    template = 'gibdd_app/Driver_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_insurance(request):
    if request.method == 'POST':
        form = InsuranceForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Insurance(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = InsuranceForm()

    template = 'gibdd_app/Insurance_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_insurance_license(request):
    if request.method == 'POST':
        form = InsuranceLicenseForm(request.POST, request.FILES)
        if form.is_valid():
            cam = InsuranceLicense(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = InsuranceLicenseForm()

    template = 'gibdd_app/InsuranceLicense_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_accident_car(request):
    if request.method == 'POST':
        form = Accident_CarForm(request.POST, request.FILES)
        if form.is_valid():
            cam = Accident_Car(**form.cleaned_data)
            cam.save()
            return redirect(reverse('workers'), args=[cam.pk])
    else:
        form = Accident_CarForm()

    template = 'gibdd_app/Accident_Car_form.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


class MedicalCertificateCreate(CreateView):
    model = MedicalCertificate
    template_name = 'gibdd_app/MedicalCertificate_form.html'
    fields = '__all__'


class MedicalCertificateUpdate(UpdateView):
    model = MedicalCertificate
    template_name = 'gibdd_app/MedicalCertificate_form.html'
    fields = '__all__'
    success_url = reverse_lazy('med_list')


class CategoryCreate(CreateView):
    model = Category
    template_name = 'gibdd_app/Category_form.html'
    fields = ['category_name', 'date_open_category']


class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'gibdd_app/Category_form.html'
    fields = ['category_name', 'date_open_category']
    success_url = reverse_lazy('categ_list')


class LicenseCreate(CreateView):
    model = License
    fields = ['driver_data', 'category_dr_license_data', 'medical_certificate_data', 'photo_dr_license',
              'series_dr_license', 'number_dr_license', 'status_dr_license',
              'date_issue_dr_license', 'date_end_dr_license', 'division_give_dr_license', 'town_dr_license']


class LicenseUpdate(UpdateView):
    model = License
    fields = ['photo_dr_license', 'series_dr_license', 'number_dr_license', 'status_dr_license',
              'date_issue_dr_license', 'date_end_dr_license', 'division_give_dr_license', 'town_dr_license']


class DriverCreate(CreateView):
    model = Driver
    fields = '__all__'


class DriverUpdate(UpdateView):
    model = Driver
    fields = '__all__'


class LicenseDisqualificationCreate(CreateView):
    model = LicenseDisqualification
    fields = '__all__'


class LicenseDisqualificationUpdate(UpdateView):
    model = LicenseDisqualification
    fields = '__all__'
