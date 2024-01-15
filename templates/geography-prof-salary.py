import math
import pandas as pd
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


def creating_tables(table):
    f1 = open(f"geography/tables/prof_top_20_cities_by_salary.html", "w", encoding='utf-8')
    f1.write(table)
    f1.close()
    return


def creating_plot(df):
    plt.figure(figsize=(16, 8))
    plt.barh(df['Город'], df['Средняя зарплата'])
    plt.tick_params(axis='y', labelrotation=0, labelsize=15)
    plt.tick_params(axis='y', labelright=False, labelleft=True)
    plt.tick_params(axis='x', labelrotation=0, labelsize=15)
    plt.title('Уровень зарплат по городам', fontdict = {'fontsize' : 24})
    plt.tight_layout()
    plt.savefig(f"geography/graph/prof_graph_top_20_cities_by_salary.png", dpi=100)
    return


def main():
    data = pd.read_csv("vacancies.csv", usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at'])
    selected_profession = 'Devops-инженер'
    data = data[data['name'].str.contains(selected_profession, case=False, na=False)]
    data = data.drop('name', axis=1)
    data = data.dropna(subset=['area_name', 'salary_from', 'salary_to', 'salary_currency']).reset_index(drop=True)
    data['published_at'] = pd.to_datetime(data['published_at'], utc=True).dt.strftime("%Y-%m")
    data = data.replace('RUR', 'RUB')
    data = data.dropna(subset=['salary_currency'])
    data[['salary_from', 'salary_to']] = data[['salary_from', 'salary_to']].fillna(value=0)
    conv = pd.read_csv('currency.csv')
    merged_df = pd.merge(data, conv, left_on='published_at', right_on='date', how='left')
    data = 0
    converted_df = merged_df.apply(convert_salary, axis=1)
    merged_df = 0
    converted_df['salary_currency'] = converted_df['salary_currency'].fillna('RUB')
    converted_df = converted_df.fillna(0)
    converted_df = converted_df.drop('published_at', axis=1)
    converted_df['average_salary'] = converted_df[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(
            math.floor).astype(int)
    df_by_city = converted_df.groupby('area_name').agg({
        'average_salary': 'mean'
    }).reset_index().dropna(subset=['average_salary'])
    df_by_city.columns = ['Город', 'Средняя зарплата']
    df_by_city['Средняя зарплата'] = df_by_city['Средняя зарплата'].apply(math.floor).astype(int)
    df_by_city = df_by_city[df_by_city['Средняя зарплата'] > 0].sort_values(by='Средняя зарплата', ascending=False)
    df_by_city = df_by_city.reset_index().drop('index', axis=1).head(20)
    creating_tables(df_by_city.to_html(index=False))
    creating_plot(df_by_city.sort_values(by='Средняя зарплата', ascending=True))
    return


if __name__ == '__main__':
    main()