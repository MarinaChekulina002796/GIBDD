from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views import View
from gibdd_app.forms import AuthorizationForm

# from channel.forms import ChannelForm, RegistrationForm, AuthorizationForm
# from channel.models import Channel, Comment, Like, Subscription
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# главная страница со списком каналов
def main(request):
    # по алфавиту по названиям
    #channels = Channel.objects.all().order_by('title')
    # page = request.GET.get('page')
    # paginator = Paginator(channels, 3)
    # try:
    #     channels = paginator.page(page)
    # except PageNotAnInteger:
    #     channels = paginator.page(1)
    # except EmptyPage:
    #     channels = paginator.page(paginator.num_pages)
    return render(request, 'gibdd_app/main.html')


def services(request):
    return render (request,'gibdd_app/services_for_drivers.html')


def gibdd(request):
    return render (request,'gibdd_app/gibdd.html')


def participants(request):
    return render (request,'gibdd_app/participants.html')


def workers(request):
    return render (request,'gibdd_app/workers.html')


def statistics(request):
    return render (request,'gibdd_app/statistics.html')


def contacts(request):
    return render (request,'gibdd_app/contacts.html')


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