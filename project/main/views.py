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


def index(request):
    posts = Person.objects.all()
    if request.user.is_authenticated:
        return main(request)
    else:
        return render(request, 'main/index.html')


def main(request):
    posts = Person.objects.all()
    gender = Gender.objects.all()

    # paginator = Paginator(posts, 1)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': 0,
        # 'page_obj': page_obj,
    }

    return render(request, 'main/main.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')


# def show_post(request, post_id):
#    return

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Регистрация")
    #     return dict(lics(context.items() + list(c_def.items())))

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


def show_post(request, post_slug):
    post = get_object_or_404(Person, slug=post_slug)
    gender = Gender.objects.all()

    context = {
        'post': post,
        'gender': gender,
        'gender_selected': post.gender_id,
    }

    return render(request, 'main/post.html', context=context)


def show_gender(request, gender_id):
    posts = Person.objects.filter(gender_id=gender_id)
    gender = Gender.objects.all()

    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': gender_id,
    }

    return render(request, 'main/main.html', context=context)


def addpage(request):
    user = User.objects.all()
    gender = Gender.objects.all()
    for p in user:
        is_have_anket = Person.objects.filter(slug_post_one=p.username)
    if(len(is_have_anket) > 0):
        context = {
            'gender': gender,
            'is_have_anket': True
        }
        return render(request, 'main/addpage.html', context=context)
    else:
        posts = Person.objects.all()
        if request.method == 'POST':
            form = AddPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('main')
        else:
            form = AddPostForm()
        context = {
            'gender': gender,
            'form': form,
            'posts': posts,
            'is_have_anket': False
        }
        return render(request, 'main/addpage.html', context=context)


def my_anket(request):
    print(User.username)
    posts = Person.objects.all()
    gender = Gender.objects.all()
    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': 0,
    }
    return render(request, 'main/my_anket.html', context=context)

def delete_anket(request):
    user = User.objects.all()
    for p in user:
        posts = Person.objects.filter(slug_post_one=p.username)
    if(len(posts)>0):
        posts.delete()
    else:
        print("нету записей")
    return main(request)

def team(request):
    return render(request, 'main/team.html')

def contacts(request):
    return render(request,'main/contacts.html')