from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import AbstractBaseUser


class Person(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="Имя")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    content = models.TextField(blank=True, verbose_name="Информация о себе")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    contacts = models.CharField(max_length=255, verbose_name="Контакты для связи")
    gender = models.ForeignKey('Gender', on_delete=models.PROTECT, verbose_name="Пол")
    slug_post_one = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Ваш логин", null=True)
    age = models.IntegerField(blank=False, verbose_name="Возраст")

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        ordering = ['-id']


class Gender(models.Model):
    gender = models.CharField(max_length=10, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.gender

    def get_absolute_url(self):
        return reverse('gender', kwargs={'gender_id': self.pk})


