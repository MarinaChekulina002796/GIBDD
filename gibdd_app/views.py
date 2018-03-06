from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.views import View

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
