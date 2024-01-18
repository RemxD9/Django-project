import pandas as pd
import math
import matplotlib.pyplot as plt


def convert_salary(row):
    # Конвертация зарплаты в рубли, если валюта не RUB
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
    # Выбранная профессия
    selected_profession = 'Devops-инженер'

    # Файл с вакансиями
    csv_file = "vacancies.csv"

    # Загрузка данных о вакансиях
    data = pd.read_csv(csv_file, usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at'])

    # Преобразование даты публикации в формат "%Y-%m"
    data['published_at'] = pd.to_datetime(data['published_at'], utc=True).dt.strftime("%Y-%m")

    # Замена 'RUR' на 'RUB'
    data = data.replace('RUR', 'RUB')

    # Загрузка данных о курсах валют
    conv = pd.read_csv('currency.csv')

    # Удаление записей с отсутствующей информацией о валюте
    data = data.dropna(subset=['salary_currency'])

    # Заполнение пропущенных значений зарплат нулями
    data[['salary_from', 'salary_to']] = data[['salary_from', 'salary_to']].fillna(value=0)

    # Объединение данных о вакансиях и курсах валют
    merged_df = pd.merge(data, conv, left_on='published_at', right_on='date', how='left')

    # Применение функции конвертации зарплаты
    converted_df = merged_df.apply(convert_salary, axis=1)

    # Заполнение пропущенных значений валюты 'RUB'
    converted_df['salary_currency'] = converted_df['salary_currency'].fillna('RUB')

    # Заполнение оставшихся пропущенных значений нулями
    converted_df = converted_df.fillna(0)

    # Добавление столбца с годом
    converted_df['Год'] = pd.to_datetime(converted_df['published_at'], utc=True).dt.year

    # Вычисление средней зарплаты
    converted_df['average_salary'] = converted_df[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(
        math.floor).astype(int)

    # Статистика по всем вакансиям
    average_salary_all = converted_df.groupby('Год').agg({'average_salary': 'mean'}).reset_index().dropna(
        subset=['average_salary'])
    average_salary_all.columns = ['Год', 'Средняя зарплата']

    # Строительство графика и сохранение в файл
    plt.figure(figsize=(16, 8))
    plt.bar(average_salary_all['Год'], average_salary_all['Средняя зарплата'])
    plt.xticks(average_salary_all['Год'])
    plt.title('Средняя зарплата по годам', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/salary-dynamic-by-year.png", dpi=100)
    plt.clf()

    # Создание HTML-таблицы и сохранение в файл
    f1 = open("popularity/tables/salary-dynamic-by-year.html", "w", encoding='utf-8')
    f1.write(average_salary_all.to_html(index=False))
    f1.close()

    # Статистика по количеству вакансий
    years_df = converted_df.groupby('Год').agg({'name': 'count'}).reset_index()
    years_df.columns = ['Год', 'Количество вакансий']

    # Строительство графика и сохранение в файл
    plt.figure(figsize=(16, 8))
    plt.bar(years_df['Год'], years_df['Количество вакансий'])
    plt.xticks(years_df['Год'])
    plt.title('Количество вакансий по годам', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/count-dynamic-by-year.png", dpi=100)
    plt.clf()

    # Создание HTML-таблицы и сохранение в файл
    f2 = open("popularity/tables/count-dynamic-by-year.html", "w", encoding='utf-8')
    f2.write(years_df.to_html(index=False))
    f2.close()

    # Статистика по выбранной профессии - средняя зарплата
    selected_profession_data = converted_df[converted_df.name.str.contains(selected_profession, na=False, case=False)]
    selected_salary_all = selected_profession_data.groupby('Год').agg({'average_salary': 'mean'}).reset_index()
    selected_salary_all.columns = ['Год', 'Средняя зарплата']

    # Строительство графика и сохранение в файл
    plt.figure(figsize=(16, 8))
    plt.bar(selected_salary_all['Год'], selected_salary_all['Средняя зарплата'])
    plt.xticks(selected_salary_all['Год'])
    plt.title('Средняя зарплата по годам для выбранной профессии', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/profession-salary-dynamic-by-year.png", dpi=100)
    plt.clf()

    # Создание HTML-таблицы и сохранение в файл
    f3 = open("popularity/tables/profession-salary-dynamic-by-year.html", "w", encoding='utf-8')
    f3.write(selected_salary_all.to_html(index=False))
    f3.close()

    # Статистика по выбранной профессии - количество вакансий
    selected_years_df = selected_profession_data.groupby('Год').agg({'name': 'count'}).reset_index()
    selected_years_df.columns = ['Год', 'Количество вакансий']

    # Строительство графика и сохранение в файл
    plt.figure(figsize=(16, 8))
    plt.bar(selected_years_df['Год'], selected_years_df['Количество вакансий'])
    plt.xticks(selected_years_df['Год'])
    plt.title('Количество вакансий по годам для выбранной профессии', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/profession-count-dynamic-by-year.png", dpi=100)

    # Создание HTML-таблицы и сохранение в файл
    f4 = open("popularity/tables/profession-count-dynamic-by-year.html", "w", encoding='utf-8')
    f4.write(selected_years_df.to_html(index=False))
    f4.close()

    return


creating_html_tables()