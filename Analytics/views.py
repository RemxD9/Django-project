from datetime import datetime
import requests
from django.shortcuts import render
from django.utils import timezone
from .models import Vacancy


def main_page(request):
    return render(request, 'mainpage.html')


def popularity(request):
    return render(request, 'popularity.html')


def geography(request):
    return render(request, 'geography.html')


def skills(request):
    return render(request, 'skills.html')


def get_hh_vacancy_description(vacancy_id):
    url = f'https://api.hh.ru/vacancies/{vacancy_id}'
    response = requests.get(url)
    data = response.json()
    return data.get('description', '')


def get_hh_vacancy_skills(vacancy_id):
    url = f'https://api.hh.ru/vacancies/{vacancy_id}/key_skills'
    response = requests.get(url)
    data = response.json()
    skills = ', '.join(skill.get('name', '') for skill in data)
    return skills


def get_hh_vacancies(profession):
    url = f'https://api.hh.ru/vacancies'
    params = {
        'text': profession,
        'area': 1,
        'period': 1,
        'per_page': 10,
        'order_by': 'published_at',
    }
    response = requests.get(url, params=params)
    data = response.json().get('items', [])

    vacancies = []
    for item in data:
        vacancy_id = item.get('id', '')
        description = get_hh_vacancy_description(vacancy_id)
        skills = get_hh_vacancy_skills(vacancy_id)

        vacancy = {
            'title': item.get('name', ''),
            'description': description,
            'skills': skills,
            'company': item.get('employer', {}).get('name', ''),
            'salary': item.get('salary', {}).get('from', ''),
            'region': item.get('area', {}).get('name', ''),
            'publication_date': datetime.fromisoformat(item.get('published_at')).replace(tzinfo=timezone.utc),
        }
        vacancies.append(vacancy)

    return vacancies


def get_hh_vacancies_for_multiple_professions(professions):
    all_vacancies = []
    for profession in professions:
        vacancies = get_hh_vacancies(profession)
        all_vacancies.extend(vacancies)
    return all_vacancies


def last_vacancies(request):
    professions = ['devops', 'development operations']
    vacancies = get_hh_vacancies_for_multiple_professions(professions)

    for vacancy_data in vacancies:
        Vacancy.objects.create(**vacancy_data)

    context = {'vacancies': Vacancy.objects.all()}
    return render(request, 'last-vacancies.html', context)
