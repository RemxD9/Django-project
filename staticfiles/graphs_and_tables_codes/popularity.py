import matplotlib.pyplot as plt
import pandas as pd


def plot_dynamic_salary(vacancies):
    plt.figure(figsize=(10, 6))
    grouped_data = vacancies.groupby('year')['salary_from'].mean().reset_index()
    plt.plot(grouped_data['year'], grouped_data['salary_from'], marker='o', label='Average Salary')
    plt.fill_between(grouped_data['year'], grouped_data['salary_from'], grouped_data['salary_to'], alpha=0.2, label='Salary Range')
    plt.title('Dynamic Salary Over Years')
    plt.xlabel('Year')
    plt.ylabel('Average Salary (RUB)')
    plt.legend()
    plt.savefig('dynamic_salary.png')


def plot_dynamic_vacancy_count(vacancies):
    plt.figure(figsize=(10, 6))
    grouped_data = vacancies.groupby('year').size().reset_index(name='count')
    plt.bar(grouped_data['year'], grouped_data['count'])
    plt.title('Dynamic Vacancy Count Over Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Vacancies')
    plt.savefig('dynamic_vacancy_count.png')


def plot_dynamic_salary_for_profession(vacancies, profession):
    plt.figure(figsize=(10, 6))
    filtered_data = vacancies[vacancies['name'].str.lower().str.contains(profession.lower())]
    grouped_data = filtered_data.groupby('year')['salary_from'].mean().reset_index()
    plt.plot(grouped_data['year'], grouped_data['salary_from'], marker='o', label='Average Salary')
    plt.fill_between(grouped_data['year'], grouped_data['salary_from'], grouped_data['salary_to'], alpha=0.2, label='Salary Range')
    plt.title(f'Dynamic Salary for {profession} Over Years')
    plt.xlabel('Year')
    plt.ylabel('Average Salary (RUB)')
    plt.legend()
    plt.savefig(f'dynamic_salary_{profession.lower()}.png')


def plot_dynamic_vacancy_count_for_profession(vacancies, profession):
    plt.figure(figsize=(10, 6))
    filtered_data = vacancies[vacancies['name'].str.lower().str.contains(profession.lower())]
    grouped_data = filtered_data.groupby('year').size().reset_index(name='count')
    plt.bar(grouped_data['year'], grouped_data['count'])
    plt.title(f'Dynamic Vacancy Count for {profession} Over Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Vacancies')
    plt.savefig(f'dynamic_vacancy_count_{profession.lower()}.png')