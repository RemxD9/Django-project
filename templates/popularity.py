import pandas as pd
import math
import matplotlib.pyplot as plt


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
    selected_profession = 'Devops-инженер'
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
    average_salary_all = converted_df.groupby('Год').agg({
        'average_salary': 'mean'
    }).reset_index().dropna(subset=['average_salary'])
    average_salary_all.columns = ['Год', 'Средняя зарплата']
    average_salary_all['Средняя зарплата'] = average_salary_all['Средняя зарплата'].apply(math.floor).astype(int)
    df1 = average_salary_all
    plt.figure(figsize=(16, 8))
    plt.bar(df1['Год'], df1['Средняя зарплата'])
    plt.xticks(df1['Год'])
    plt.title('Средняя зарплата по годам', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/salary-dynamic-by-year.png", dpi=100)
    plt.clf()
    f1 = open("popularity/tables/salary-dynamic-by-year.html", "w", encoding='utf-8')
    f1.write(df1.to_html(index=False))
    f1.close()
    years_df = converted_df.groupby('Год').agg({'name': 'count'}).reset_index()
    years_df.columns = ['Год', 'Количество вакансий']
    df2 = years_df
    plt.figure(figsize=(16, 8))
    plt.bar(df2['Год'], df2['Количество вакансий'])
    plt.xticks(df2['Год'])
    plt.title('Количество вакансий по годам', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/count-dynamic-by-year.png", dpi=100)
    plt.clf()
    f2 = open("popularity/tables/count-dynamic-by-year.html", "w", encoding='utf-8')
    f2.write(df2.to_html(index=False))
    f2.close()
    selected_profession_data = converted_df[converted_df.name.str.contains(selected_profession, na=False, case=False)]
    selected_salary_all = selected_profession_data.groupby('Год').agg({'average_salary': 'mean'}).reset_index()
    selected_salary_all.columns = ['Год', 'Средняя зарплата']
    selected_salary_all['Средняя зарплата'] = selected_salary_all['Средняя зарплата'].apply(math.floor).astype(int)
    df3 = selected_salary_all
    plt.figure(figsize=(16, 8))
    plt.bar(df3['Год'], df3['Средняя зарплата'])
    plt.xticks(df3['Год'])
    plt.title('Средняя зарплата по годам для выбранной профессии', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/profession-salary-dynamic-by-year.png", dpi=100)
    plt.clf()
    f3 = open("popularity/tables/profession-salary-dynamic-by-year.html", "w", encoding='utf-8')
    f3.write(df3.to_html(index=False))
    f3.close()
    selected_years_df = selected_profession_data.groupby('Год').agg({'name': 'count'}).reset_index()
    selected_years_df.columns = ['Год', 'Количество вакансий']
    df4 = selected_years_df
    plt.figure(figsize=(16, 8))
    plt.bar(df4['Год'], df4['Количество вакансий'])
    plt.xticks(df4['Год'])
    plt.title('Количество вакансий по годам для выбранной профессии', fontdict={'fontsize': 24})
    plt.tight_layout()
    plt.savefig(f"popularity/graphs/profession-count-dynamic-by-year.png", dpi=100)
    f4 = open("popularity/tables/profession-count-dynamic-by-year.html", "w", encoding='utf-8')
    f4.write(df4.to_html(index=False))
    f4.close()
    return


creating_html_tables()
