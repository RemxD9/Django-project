import matplotlib.pyplot as plt
import pandas as pd


# Функция для создания HTML-таблицы
def creating_tables(table):
    f1 = open(f"geography/tables/prof_top_20_cities_by_rate.html", "w", encoding='utf-8')
    f1.write(table)  # Записываем таблицу в файл
    f1.close()
    return


# Функция для создания графика
def creating_plot(df):
    plt.figure(figsize=(16, 8))  # Устанавливаем размер графика
    plt.barh(df['Город'], df['Доля вакансий, %'])  # Строим горизонтальную столбчатую диаграмму
    plt.tick_params(axis='y', labelrotation=0, labelsize=15)  # Настройка меток по оси Y
    plt.tick_params(axis='y', labelright=False, labelleft=True)
    plt.tick_params(axis='x', labelrotation=0, labelsize=15)  # Настройка меток по оси X
    plt.title('Доля вакансий по городам для выбранной профессии', fontdict={'fontsize': 24})  # Заголовок графика
    plt.tight_layout()  # Улучшение отображения
    plt.savefig(f"geography/graphs/prof_graph_top_20_cities_by_rate.png", dpi=100)  # Сохранение графика в файл
    return


# Основная функция
def main():
    # Загрузка данных о вакансиях из CSV-файла
    df2 = pd.read_csv("vacancies.csv", usecols=['name', 'area_name', 'published_at'])
    count = len(df2)
    selected_profession = 'Devops-инженер'
    df2 = df2[df2['name'].str.contains(selected_profession, case=False, na=False)]
    df2 = df2.drop('name', axis=1)

    # Расчет доли вакансий по городам
    df2['rate'] = df2.groupby('area_name')['area_name'].transform(lambda x: x.count() / count * 100)
    df_by_city_rate = df2.groupby('area_name').agg({
        'rate': 'first'
    }).reset_index()

    # Настройка названий колонок
    df_by_city_rate.columns = ['Город', 'Доля вакансий, %']
    df_by_city_rate = df_by_city_rate[df_by_city_rate['Доля вакансий, %'] > 0].sort_values(by='Доля вакансий, %', ascending=False).reset_index().drop('index', axis=1).head(20)

    # Создание таблицы и графика
    creating_tables(df_by_city_rate.to_html(index=False))
    creating_plot(df_by_city_rate.sort_values(by='Доля вакансий, %', ascending=True))


if __name__ == '__main__':
    main()
