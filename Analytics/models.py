from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.html import format_html


# Модель пользователя, расширяющая AbstractUser Django
class SiteUser(AbstractUser):
    # Дополнительные поля пользователя
    email = models.EmailField(unique=True, default='')
    password = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=128, null=True, unique=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    # Поле, используемое для входа пользователя (логин)
    USERNAME_FIELD = 'username'
    # Обязательные поля при создании пользователя
    REQUIRED_FIELDS = ['email']

    # Свойства, указывающие на то, что пользователь не является анонимным и аутентифицирован
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    # Отображение имени пользователя в админке Django
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'site_users'


# Модель для представления вакансий
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


# Модель для представления востребованности
class Popularity(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='staticfiles/popularity/graphs', null=True)
    table = models.FileField(verbose_name='Таблица', upload_to='staticfiles/popularity/tables', null=True)

    # Метод для отображения содержимого текстового файла в админке Django
    def display_text_file(self):
        with open(self.table.path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return format_html(html_content)

    class Meta:
        verbose_name = 'Востребованность'
        verbose_name_plural = 'Востребованности'
        db_table = 'popularity'


# Модель для представления географии
class Geography(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='staticfiles/geography/graphs', null=True)
    table = models.FileField(verbose_name='Таблица', upload_to='staticfiles/geography/tables', null=True)

    # Метод для отображения содержимого текстового файла в админке Django
    def display_text_file(self):
        with open(self.table.path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return format_html(html_content)

    class Meta:
        verbose_name = 'География'
        verbose_name_plural = 'География'
        db_table = 'geography'


# Модель для представления навыков
class Skills(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='staticfiles/skills/graphs', null=True)
    table = models.FileField(verbose_name='Таблица', upload_to='staticfiles/skills/tables', null=True)

    # Метод для отображения содержимого текстового файла в админке Django
    def display_text_file(self):
        with open(self.table.path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return format_html(html_content)

    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = 'Навыки'
        db_table = 'Skills'


# Модель для представления навыков по профессии
class ProfSkills(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='staticfiles/skills/graphs', null=True)
    table = models.FileField(verbose_name='Таблица', upload_to='staticfiles/skills/tables', null=True)

    # Метод для отображения содержимого текстового файла в админке Django
    def display_text_file(self):
        with open(self.table.path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return format_html(html_content)

    class Meta:
        verbose_name = 'Навыки по профессии'
        verbose_name_plural = 'Навыки по профессии'
        db_table = 'prof-Skills'