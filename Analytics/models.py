from django.contrib.auth.models import AbstractUser, Group
from django.db import models
import pandas as pd
from django.utils.html import format_html


class SiteUser(AbstractUser):
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128, null=True, unique=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'username'  # Укажите поле, используемое в качестве уникального идентификатора
    REQUIRED_FIELDS = ['email']

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'site_users'


class Vacancy(models.Model):
    title = models.TextField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание', max_length=3000)
    skills = models.CharField(verbose_name='Навыки', max_length=255)
    company = models.CharField(verbose_name='Компания', max_length=255)
    salary = models.CharField(verbose_name='Зарплата', max_length=25)
    area_name = models.CharField(verbose_name='Местоположение', max_length=255)
    published_at = models.TextField(verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        db_table = 'vacancies'


class Popularity(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='staticfiles', null=True)
    table = models.FileField(verbose_name='Таблица', null=True)

    def display_text_file(self):
        with open(self.table.path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return format_html(html_content)

    class Meta:
        verbose_name = 'Востребованность'
        verbose_name_plural = 'Востребованности'
        db_table = 'popularity'


class Geography(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='staticfiles', null=True)
    table = models.FileField(verbose_name='Таблица', null=True)

    def display_text_file(self):
        with open(self.table.path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return format_html(html_content)

    class Meta:
        verbose_name = 'География'
        verbose_name_plural = 'География'
        db_table = 'geography'
