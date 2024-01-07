import pandas as pd
import math


selected_profession = 'devops'
data = pd.read_csv('vacancies.csv', delimiter=',',
                   usecols=['name', 'salary_from', 'salary_to', 'salary_currency', 'published_at'])
data = data.fillna(0)
data['Год'] = pd.to_datetime(data['published_at'], utc=True).dt.year
data['average_salary'] = data[['salary_from', 'salary_to']].mean(axis=1, skipna=True).apply(math.floor).astype(int)
years = sorted(data['Год'].unique())
average_salary_all = data.groupby('Год')['average_salary'].mean().to_frame()  # зарплата по годам
selected_profession_data = data[data.name.str.contains(selected_profession, na=False, case=False)]
selected_salary_all = selected_profession_data.groupby('Год')[
    'average_salary'].mean().to_frame()  # зарплата по годам выбранная
years_df = data.groupby('Год')['name'].count().reset_index()  # кол-во вакансий по годам
vacancies_all_count = years_df['name'].tolist()
vacancies_count_profession_by_year = selected_profession_data.groupby('Год')['name'].count().reset_index()
vacancies_count_profession_by_year = vacancies_count_profession_by_year.rename(
    columns={'name': 'Кол-во вакансий'})  # кол-во вакансий по годам для профессии
df1 = average_salary_all.reset_index().to_html()
df2 = selected_salary_all.reset_index().to_html()
df3 = years_df.set_index('Год').reset_index().to_html()
df4 = vacancies_count_profession_by_year.to_html()
html_file = open('salary-dynamic-by-year.html', 'w', encoding='utf-8')
html_file.write(df1)
html_file.close()
html_file = open('count-dynamic-by-year.html', 'w', encoding='utf-8')
html_file.write(df2)
html_file.close()
html_file = open('profession-salary-dynamic-by-year.html', 'w', encoding='utf-8')
html_file.write(df3)
html_file.close()
html_file = open('profession-count-dynamic-by-year.html', 'w', encoding='utf-8')
html_file.write(df4)
html_file.close()
