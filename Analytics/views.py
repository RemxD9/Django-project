from datetime import datetime, timedelta
import requests
from django.contrib.auth.decorators import login_required
from .models import Vacancy, Geography, Popularity, Skills, ProfSkills
import re
import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm


# Функция для выхода пользователя из системы
def logout_view(request):
    logout(request)
    return redirect('login_view')


# Функция для обработки регистрации нового пользователя
def registration_view(request):
    # Проверка, аутентифицирован ли уже пользователь
    if request.user.is_authenticated:
        return redirect('user_profile')

    # Обработка POST-запроса при отправке формы регистрации
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Сохранение пользователя и добавление в выбранную группу
            user = form.save()
            selected_group = form.cleaned_data['group']
            user.groups.add(selected_group)
            login(request, user)
            return redirect('user_profile')
        else:
            # Отображение формы с сообщением об ошибке
            return render(request, 'registration/register.html', {'form': form, 'error_message': 'Заполните обязательные поля'})
    else:
        form = RegistrationForm()

    # Отображение формы регистрации
    return render(request, 'registration/register.html', {'form': form})


# Функция для обработки входа пользователя
def login_view(request):
    error_message = None  # Инициализация переменной ошибки

    # Обработка POST-запроса при отправке формы входа
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')
            else:
                error_message = 'Пользователя с такими данными не существует.'
    else:
        form = AuthenticationForm()

    # Отображение формы входа с сообщением об ошибке
    return render(request, 'registration/login1.html', {'form': form, 'error_message': error_message})


# Функция для отображения профиля пользователя (требует аутентификации)
@login_required
def user_profile(request):
    return render(request, 'registration/user_profile.html')


# Функция для отображения главной страницы
def main_page(request):
    return render(request, 'main-page.html')


# Функция для отображения страницы с данными о востребованности
def popularity(request):
    popularities = Popularity.objects.all()
    return render(request, 'popularity/popularity.html', context={'popularities': popularities})


# Функция для отображения страницы с данными о географии
def geography(request):
    geographies = Geography.objects.all()
    return render(request, 'geography/geography.html', context={'geography': geographies})


# Функция для отображения страницы с данными о навыках и профессиональных навыках
def skills(request):
    skills = Skills.objects.all()
    profskills = ProfSkills.objects.all()
    return render(request, 'skills/skills.html',  context={'skills': skills, 'profskills': profskills})


# Функция для обработки и отображения списка последних вакансий
def last_vacancies(request):
    Vacancy.objects.all().delete()
    # API HH URL
    hh_api_url = 'https://api.hh.ru/vacancies'

    # Заголовок запроса
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Параметры запроса: профессия и период (24 часа назад до текущего момента)
    profession = 'DevOps-инженер'  # Здесь нужно указать выбранную профессию
    period = 24

    date_from = datetime.now() - timedelta(hours=period)

    # Опции запроса
    params = {
        'text': profession,
        'date_from': date_from.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'per_page': 10,
        'order_by': 'publication_time'
    }

    # Отправка GET-запроса к API HH
    response = requests.get(hh_api_url, params=params, headers=headers)
    data = response.json()
    vacancies_data = json.loads(response.content)
    # Обработка данных о вакансиях
    vacancies_list = []
    for vacancy_data in vacancies_data['items']:
        salary = vacancy_data['salary']
        key_skills = get_vacancy_skills(vacancy_data['url'])
        if salary:
            if salary['from'] and salary['to']:
                result_salary = f'{salary["from"]} - {salary["to"]} ({salary["currency"]})'
            elif salary['from']:
                result_salary = f'{salary["from"]}  ({salary["currency"]})'
            else:
                result_salary = f'{salary["to"]}  ({salary["currency"]})'
        else:
            result_salary = 'Зарплата не указана'
        if key_skills:
            result_skills = key_skills
        else:
            result_skills = 'Навыки не указаны'
        vacancy = Vacancy()
        vacancy.title = vacancy_data['name']
        vacancy.description = get_vacancy_description(vacancy_data['url'])
        vacancy.skills = result_skills
        vacancy.company = vacancy_data['employer']['name']
        vacancy.salary = result_salary
        vacancy.area_name = vacancy_data['area']['name']
        vacancy.published_at = datetime.strptime(vacancy_data['published_at'], '%Y-%m-%dT%H:%M:%S%z')

        vacancies_list.append(vacancy)
    for i in vacancies_list:
        if Vacancy.objects.filter(
                title=i.title,
                description=i.description,
                company=i.company,
                skills=i.skills,
                area_name=i.area_name
        ).exists():
            vacancies_list.remove(i)
    # Сохранение вакансий в базе данных
    Vacancy.objects.bulk_create(vacancies_list)

    # Получение и отображение списка последних вакансий
    last_vacancies = Vacancy.objects.order_by('-published_at')[:10]

    return render(request, 'last_vacancies/last-vacancies.html', {'last_vacancies': last_vacancies})


# Функция для получения описания вакансии по URL
def get_vacancy_description(vacancy_url):
    # Отправка GET-запроса к API HH для получения данных о вакансии
    response = requests.get(vacancy_url)
    vacancy_data = response.json()

    return re.sub(r'<[^>]+>', '', vacancy_data['description']).replace('&quot;', '.')


# Функция для получения ключевых навыков вакансии по URL
def get_vacancy_skills(vacancy_url):
    # Отправка GET-запроса к API HH для получения данных о вакансии
    response = requests.get(vacancy_url)
    vacancy_data = response.json()
    skills = []

    for skill_data in vacancy_data['key_skills']:
        skills.append(skill_data['name'])

    return ', '.join(skills)
