from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-input', 'autocomplete': 'on'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


# class AddPostForm(forms.Form):
#     first_name = forms.CharField(max_length=100, label="Имя")
#     last_name = forms.CharField(max_length=100, label="Фамилия")
#     content = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}), label="Информация о себе")
#     contacts = forms.CharField(max_length=255, label="Контакты для связи")
#     is_published = forms.BooleanField(label="Публикация", initial=True)
#     gender = forms.ModelChoiceField(queryset=Gender.objects.all(), label="Пол", empty_label="Категория не выбрана")

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].empty_label = "Пол не выбран"

    class Meta:
        model = Person
        
        fields = ['first_name', 'last_name','age', 'slug', 'content', 'contacts', 'photo', 'is_published', 'gender', 'slug_post_one']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 100, 'rows': 5}),
            'slug_post_one': forms.Textarea(attrs={'placeholder': "свой логин", 'cols': 20, 'rows': 1.5})
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) > 100:
            raise ValidationError("Длина имени превышает 100 символов")

        return first_name

    def clean_slug_post_one(self):
        print("заходит")
        slug_post_one = self.cleaned_data['slug_post_one']
        is_correct = True
        user = User.objects.all()
        for p in user:
            if slug_post_one == p.username:
                is_correct = False
        if is_correct:
            raise ValidationError("Введите свой логин")

        return slug_post_one

    def clean_age(self):
        age = self.cleaned_data['age']
        if (age < 0) or (age>50):
            raise ValidationError("Введите настоящий возраст")

        return age