import django.contrib.auth
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.mail import send_mail

def index(request):
    if request.user.is_authenticated:
        return main(request)
    else:
        return render(request, 'main/index.html')

def main(request):

    context = {
    }

    return render(request, 'main/main.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('main')

def Logout_User(request):
    logout(request)
    return redirect('login')
