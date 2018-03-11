# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from gibdd_app.forms import AuthorizationForm, MedicalCertificateForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from gibdd_app.models import MedicalCertificate, License, Category, Driver, LicenseDisqualification
from django.shortcuts import render


# главная страница ГИБДД
def main(request):
    return render(request, 'gibdd_app/main.html')


# список всех справок (по 2 шт в ряд)
def med_list(request):
    template = 'gibdd_app/MedicalCertificate_list.html'
    objects_list = MedicalCertificate.objects.all()

    context = {
        'objects_list': objects_list,
    }
    return render(request, template, context)


def med_detail(request, pk):
    template = 'gibdd_app/MedicalCertificate_detail.html'

    obj = get_object_or_404(MedicalCertificate, pk=pk)
    context = {
        'obj': obj,
    }
    return render(request, template, context)


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


def services(request):
    return render(request, 'gibdd_app/services_for_drivers.html')


def gibdd(request):
    return render(request, 'gibdd_app/gibdd.html')


def participants(request):
    return render(request, 'gibdd_app/participants.html')


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

    # @login_required
    # def add_med(request):
    #     if request.method == 'POST':
    #         form = MedicalCertificateForm(request.POST, request.FILES)  # тут возвращается словарь вместе с csrf
    #         if form.is_valid():
    #             med = MedicalCertificate(**form.cleaned_data)
    #             med.save()
    #             messages.success(request, 'Your MedicalCertificate Was Successfully Saved')
    #             return redirect(reverse('workers'), args=[med.pk])
    #     else:
    #         form = MedicalCertificateForm()
    #         messages.warning(request, "MedicalCertificate Failed To Save. Error")
    #
    #     template = 'gibdd_app/MedicalCertificate_form.html'
    #     context = {
    #         'form': form,
    #     }
    #
    #     return render(request, template, context)

    #
    # @login_required
    # def update_med(request, pk):
    #     med = get_object_or_404(MedicalCertificate, pk=pk)
    #     # med=MedicalCertificate.objects.get(pk=pk)
    #     if request.method == 'POST':
    #         form = MedicalCertificateForm(request.POST, request.FILES, instance=med)
    #         if form.is_valid():
    #             form.save()
    #     else:
    #         form = MedicalCertificateForm(instance=med)
    #
    #     template = 'gibdd_app/MedicalCertificate_form.html'
    #     # context = {
    #     #     'form': form,
    #     #     'med': med,}
    #     #
    #     context={
    #         'form':form,
    #         'med':med,
    #     }
    #
    #     return render(request, template, context)


class MedicalCertificateCreate(CreateView):
    model = MedicalCertificate
    template_name = 'gibdd_app/MedicalCertificate_form.html'
    fields = '__all__'


class MedicalCertificateUpdate(UpdateView):
    model = MedicalCertificate
    template_name = 'gibdd_app/MedicalCertificate_form.html'
    fields = '__all__'
    success_url = reverse_lazy('main')


class LicenseCreate(CreateView):
    model = License
    fields = ['driver_data', 'category_dr_license_data', 'medical_certificate_data', 'photo_dr_license',
              'series_dr_license', 'number_dr_license', 'status_dr_license',
              'date_issue_dr_license', 'date_end_dr_license', 'division_give_dr_license', 'town_dr_license']


class LicenseUpdate(UpdateView):
    model = License
    fields = ['photo_dr_license', 'series_dr_license', 'number_dr_license', 'status_dr_license',
              'date_issue_dr_license', 'date_end_dr_license', 'division_give_dr_license', 'town_dr_license']

    # class LicenseDelete(DeleteView):
    #     model = License
    #     success_url = reverse_lazy('main')
    #
    # class CategoryCreate(CreateView):
    #     model = Category
    #     fields = ['category_name', 'contents_category', 'date_open_category']
    #
    # class CategoryUpdate(UpdateView):
    #     model = Category
    #     fields = ['category_name', 'contents_category', 'date_open_category']
    #
    # class CategoryDelete(DeleteView):
    #     model = Category
    #     success_url = reverse_lazy('main')
