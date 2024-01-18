import pandas as pd
import matplotlib.pyplot as plt


def main():
    # Считываем данные, используя только необходимые столбцы
    data = pd.read_csv("vacancies.csv", usecols=['name', 'key_skills', 'published_at'])

    # Удаление записей с отсутствующими значениями в столбцах 'name' и 'key_skills'
    data.dropna(subset=['name', 'key_skills'], inplace=True)

    # Выбор конкретной профессии
    selected_profession = 'Devops-инженер'
    data = data[data['name'].str.contains(selected_profession, na=False, case=False)]

    # Преобразование даты публикации в год
    data['published_at'] = pd.to_datetime(data['published_at'], utc=True).dt.year

    # Получение списка уникальных годов
    years_list = sorted(data['published_at'].unique())

    # Создание таблиц и графиков для каждого года
    creating_skills_for_years(data, years_list)
    return


def creating_skills_for_years(data, years_list):
    for year in years_list:
        # Получение списка наиболее востребованных навыков для каждого года
        years_skills_list = (data[data['published_at'] == year]['key_skills'].str.split(',|\n', expand=True)
                             .stack().value_counts().nlargest(20))

        # Пропуск итерации, если список навыков пуст
        if years_skills_list.size == 0:
            continue

        # Создание DataFrame с наиболее востребованными навыками
        top_skills = pd.DataFrame({'Навык': years_skills_list.index, 'Количество': years_skills_list.values})

        # Создание графика
        creating_plot(top_skills, str(year))

        # Создание HTML-таблицы и сохранение в файл
        creating_html_tables(str(year), top_skills.to_html(index=False))
    return


def creating_plot(df, year):
    # Создание горизонтального бар-графика
    fig, ax = plt.subplots()
    bars = ax.barh(df['Навык'], df['Количество'])

    # Настройки отображения графика
    ax.tick_params(axis='y', labelrotation=0, labelsize=8)
    ax.tick_params(axis='y', labelright=False, labelleft=True)

    # Добавление заголовка
    plt.title(year)

    # Сохранение графика в файл
    plt.tight_layout()
    plt.savefig(f"skills/graphs/graph_prof_top_20_by_{year}.png")
    return


def creating_html_tables(year, table):
    # Создание HTML-таблицы и сохранение в файл
    f1 = open(f"skills/tables/prof_top_20_by_{year}.html", "w", encoding='utf-8')
    f1.write(table)
    f1.close()
    return


if __name__ == '__main__':
    main()
