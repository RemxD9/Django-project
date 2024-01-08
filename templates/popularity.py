import numpy as np
import pandas as pd
import math


def convert_salary(row):
    if row['salary_currency'] != 'RUB':
        currency = row['salary_currency']
        salary_from = row['salary_from']
        salary_to = row['salary_to']
        exchange_rate = row[currency]

        if pd.notnull(salary_from):
            salary_from_rub = salary_from * exchange_rate
            row['salary_from'] = salary_from_rub

        if pd.notnull(salary_to):
            salary_to_rub = salary_to * exchange_rate
            row['salary_to'] = salary_to_rub

    return row


def creating_html_tables():
    selected_profession = 'devops'
    csv_file = "vacancies.csv"
    data = pd.read_csv(csv_file, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at'])
    data['published_at'] = pd.to_datetime(data['published_at'], utc=True).dt.strftime("%Y-%m")
    data = data.replace('RUR', 'RUB')
    conv = pd.read_csv('currency.csv')
    data = data.dropna(subset=['salary_currency'])
    data[['salary_from', 'salary_to']] = data[['salary_from', 'salary_to']].fillna(value=0)
    merged_df = pd.merge(data, conv, left_on='published_at', right_on='date', how='left')
    converted_df = merged_df.apply(convert_salary, axis=1)
    converted_df['salary_currency'] = converted_df['salary_currency'].fillna('RUB')
    converted_df = converted_df.fillna(0)
    converted_df['Год'] = pd.to_datetime(converted_df['published_at'], utc=True).dt.year
    converted_df['average_salary'] = converted_df[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(
        math.floor).astype(
        int)
    years = sorted(converted_df['Год'].unique())
    average_salary_all = converted_df.groupby('Год')['average_salary'].mean().apply(math.floor).astype(
        int).to_frame()  # зарплата по годам
    selected_profession_data = converted_df[converted_df.name.str.contains(selected_profession, na=False, case=False)]
    selected_salary_all = selected_profession_data.groupby('Год')[
        'average_salary'].mean().astype(int).to_frame()  # зарплата по годам выбранная
    years_df = converted_df.groupby('Год')['name'].count().reset_index()  # кол-во вакансий по годам
    vacancies_all_count = years_df['name'].tolist()
    vacancies_count_profession_by_year = selected_profession_data.groupby('Год')['name'].count().reset_index()
    vacancies_count_profession_by_year = vacancies_count_profession_by_year.rename(
        columns={'name': 'count'})  # кол-во вакансий по годам для профессии
    df1 = average_salary_all.reset_index().to_html()  # зп для всех
    df2 = years_df.set_index('Год').rename(
        columns={'name': 'vacancy_count'}).reset_index().to_html()  # кол-во вакансии
    df3 = selected_salary_all.reset_index().to_html()  # зп для профессии
    df4 = vacancies_count_profession_by_year.to_html()  # выбранная вакансия
    f1 = open("popularity/salary-dynamic-by-year.html", "w", encoding='utf-8')
    f1.write(df1)
    f1.close()
    f2 = open("popularity/count-dynamic-by-year.html", "w", encoding='utf-8')
    f2.write(df2)
    f2.close()
    f3 = open("popularity/profession-salary-dynamic-by-year.html", "w", encoding='utf-8')
    f3.write(df3)
    f3.close()
    f4 = open("popularity/profession-count-dynamic-by-year.html", "w", encoding='utf-8')
    f4.write(df4)
    f4.close()
    return


creating_html_tables()