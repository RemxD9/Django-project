import pandas as pd
from popularity import plot_dynamic_salary, plot_dynamic_vacancy_count, plot_dynamic_salary_for_profession, \
    plot_dynamic_vacancy_count_for_profession
from currency_converter import convert_salary_range_to_rubles, convert_salary_to_rubles


def load_data():
    # Загрузим данные из файла CSV
    data = pd.read_csv('C:/Users/acer/Desktop/vacancies/vacancies.csv', delimiter=',')
    return data


def preprocess_data(vacancies):
    # Предобработка данных
    vacancies['published_at'] = pd.to_datetime(vacancies['published_at'], utc=True)
    vacancies['year'] = vacancies['published_at'].dt.year

    # Конвертация зарплат и вилки зарплат в рубли
    for i, row in vacancies.iterrows():
        vacancies.at[i, 'salary'] = convert_salary_to_rubles(row['salary'], row['currency'])
        vacancies.at[i, 'salary_range'] = convert_salary_range_to_rubles(row['salary_range'], row['currency'],
                                                                         row['published_at'])

    # Разделим salary и salary_range на отдельные столбцы
    vacancies[['salary_from', 'salary_to']] = pd.DataFrame(vacancies['salary'].tolist(), index=vacancies.index)
    vacancies[['salary_range_from', 'salary_range_to']] = pd.DataFrame(vacancies['salary_range'].tolist(),
                                                                       index=vacancies.index)

    return vacancies


def demand():
    # Загрузка и предобработка данных
    vacancies = load_data()
    vacancies = preprocess_data(vacancies)

    # Построение графиков и сохранение в файл
    plot_dynamic_salary(vacancies)
    plot_dynamic_vacancy_count(vacancies)
    # Построение графиков по ключевым словам и сохрание их в файл
    plot_dynamic_salary_for_profession(vacancies, 'devops')
    plot_dynamic_vacancy_count_for_profession(vacancies, 'devops')
    plot_dynamic_salary_for_profession(vacancies, 'development operations')
    plot_dynamic_vacancy_count_for_profession(vacancies, 'development operations')


demand()
