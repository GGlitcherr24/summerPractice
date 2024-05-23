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

# Первых заход на сайт, если авторизирован на главную, если нет то на страницу регистрации и никуда больше
def index(request):
    posts = Person.objects.all()
    if request.user.is_authenticated:
        return main(request)
    else:
        return render(request, 'main/index.html')


# Переход на главную страницу
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


# Ошибка при неправильной ссылке
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')


# def show_post(request, post_id):
#    return

# Переход на страницу регистрации
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


# Переход на страницу авторизации
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('main')


# Выход из аккаунта
def Logout_User(request):
    logout(request)
    return redirect('login')


# Отображение всех анкет
def show_post(request, post_slug):
    post = get_object_or_404(Person, slug=post_slug)
    gender = Gender.objects.all()

    context = {
        'post': post,
        'gender': gender,
        'gender_selected': post.gender_id,
    }

    return render(request, 'main/post.html', context=context)


# Фильтр по возрасту
def show_age(request, age, gender_id=None):
    age_control = []
    match age:
        case 18:
            age_control = [int(i) for i in range(18)]
        case 25:
            age_control = [int(i) for i in range(18, 26)]
        case 35:
            age_control = [int(i) for i in range(26, 36)]
        case 50:
            age_control = [int(i) for i in range(36, 51)]

    gender = Gender.objects.all()
    if gender_id is not None:
        posts = Person.objects.filter(age__in=age_control) & Person.objects.filter(gender_id=gender_id)
        context = {
            'posts': posts,
            'gender': gender,
            'gender_selected': gender_id,
            'age': age,
        }
    else:
        posts = Person.objects.filter(age__in=age_control)
        context = {
            'posts': posts,
            'gender': gender,
            'gender_selected': 0,
            'age': age,
        }

    return render(request, 'main/main.html', context=context)


# Фильтр по гендеру
def show_gender(request, gender_id):
    posts = Person.objects.filter(gender_id=gender_id)
    gender = Gender.objects.all()

    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': gender_id,
    }

    return render(request, 'main/main.html', context=context)


# Добавление анкеты
def addpage(request):
    user = User.objects.all()
    gender = Gender.objects.all()
    for p in user:
        is_have_anket = Person.objects.filter(slug_post_one=p.username)
    if (len(is_have_anket) > 0):
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


# Просмотр своей анекты
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


# Удаление анкеты
def delete_anket(request):
    user = User.objects.all()
    for p in user:
        posts = Person.objects.filter(slug_post_one=p.username)
    if (len(posts) > 0):
        posts.delete()
    else:
        print("нету записей")
    return main(request)


# Переход на страницу информации о команде
def team(request):
    return render(request, 'main/team.html')


# Переход на страницу информации о контактах разработчиков
def contacts(request):
    return render(request, 'main/contacts.html')


# Поиск по словам для модератора
def find_bad_content(request):
    if request.method == 'POST':
        search = request.POST.get('search_input')
        person = Person.objects.all()
        for p in person:
            posts = Person.objects.filter(content__icontains=search)
        gender = Gender.objects.all()
        context = {
            'posts': posts,
            'gender': gender,
        }

    return render(request, 'main/main.html', context=context)


# Полное удаление аккаунта модером или администратором
def admin_delete_account(request, post_slug, slug_post_one):
    try:
        anket = Person.objects.get(slug=post_slug)
        user = User.objects.get(username=slug_post_one)
        anket.delete()
        user.delete()
    except User.DoesNotExist:
        print("Пользователь не найден")

    posts = Person.objects.all()
    gender = Gender.objects.all()

    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': 0,
        # 'page_obj': page_obj,
    }
    return render(request, 'main/main.html', context=context)

# Переход на страницу отправки вопроса
def question_for_admin(request):
    context = {
        'success': 2
    }
    return render(request, 'main/question_for_admin.html', context=context)

#Метод отправляющий вопрос
def send_question(request):
    recipient_list = ['dasha.belosludtseva.03@mail.ru']
    success = 2
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        try:
            send_mail(
                subject=f'Новое сообщение с сайта от {name}',
                message=f'Имя отправителя: {name} \n Email отправителя: {email} \n Сообщение:{message}',
                from_email=email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            success = 1
        except Exception as e:
            print(e)
            success = 0

    context = {
        'success': success
    }
    return render(request, 'main/question_for_admin.html', context=context)

#Фильтр по хобби
def filter_hobby(request, hobby):
    hobby = hobby[1:-1]
    posts = Person.objects.filter(hobby=hobby)
    gender = Gender.objects.all()
    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': 0,
        'hobby': hobby
    }
    return render(request, 'main/main.html', context=context)

def filter_hobby_and_gender_id(request, gender_id, hobby):
    hobby = hobby[1:-1]
    print(gender_id, hobby)
    posts = Person.objects.filter(hobby=hobby) & Person.objects.filter(gender_id=gender_id)
    gender = Gender.objects.all()
    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': gender_id,
        'hobby': hobby
    }
    return render(request, 'main/main.html', context=context)

def filter_hobby_and_age(request, age, hobby):
    print(hobby, age)
    age_control = []
    match age:
        case 18:
            age_control = [int(i) for i in range(18)]
        case 25:
            age_control = [int(i) for i in range(18, 26)]
        case 35:
            age_control = [int(i) for i in range(26, 36)]
        case 50:
            age_control = [int(i) for i in range(36, 51)]

    posts = Person.objects.filter(hobby=hobby) & Person.objects.filter(age__in=age_control) & Person.objects.filter(
        age__lte=20)
    gender = Gender.objects.all()
    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': 0,
        'age': age,
        'hobby': hobby
    }
    return render(request, 'main/main.html', context=context)

def filter_hobby_age_gender(request, gender_id, age, hobby):
    print(hobby, gender_id, age)
    age_control = []
    match age:
        case 18:
            age_control = [int(i) for i in range(18)]
        case 25:
            age_control = [int(i) for i in range(18, 26)]
        case 35:
            age_control = [int(i) for i in range(26, 36)]
        case 50:
            age_control = [int(i) for i in range(36, 51)]
    if gender_id != 0:
        posts = Person.objects.filter(hobby=hobby) & Person.objects.filter(age__in=age_control) & Person.objects.filter(
            gender_id=gender_id)
    else:
        posts = Person.objects.filter(hobby=hobby) & Person.objects.filter(age__in=age_control)
    gender = Gender.objects.all()
    context = {
        'posts': posts,
        'gender': gender,
        'gender_selected': gender_id,
        'age': age,
        'hobby': hobby
    }
    return render(request, 'main/main.html', context=context)