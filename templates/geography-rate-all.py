import matplotlib.pyplot as plt    
import pandas as pd


def creating_tables(table):
    # Открываем файл для записи HTML-таблицы с информацией о вакансиях по городам
    f1 = open(f"geography/tables/top_20_cities_by_rate.html", "w", encoding='utf-8')
    f1.write(table)  # Записываем HTML-таблицу в файл
    f1.close()
    return

def creating_plot(df):
    # Создаем горизонтальную столбчатую диаграмму с долей вакансий по городам
    plt.figure(figsize=(16, 8))
    plt.barh(df['Город'], df['Доля вакансий, %'])
    plt.tick_params(axis='y', labelrotation=0, labelsize=15)  # Настройка меток по оси Y
    plt.tick_params(axis='y', labelright=False, labelleft=True)
    plt.tick_params(axis='x', labelrotation=0, labelsize=15)  # Настройка меток по оси X
    plt.title('Доля вакансий по городам', fontdict={'fontsize': 24})  # Установка заголовка графика
    plt.tight_layout()  # Улучшение отображения
    plt.savefig(f"geography/graphs/graph_top_20_cities_by_rate.png", dpi=100)  # Сохранение графика в файл
    return

def main():
    # Загружаем данные о вакансиях из CSV-файла, используя только необходимые колонки
    df2 = pd.read_csv("vacancies.csv", usecols=['area_name', 'published_at'])
    count = len(df2)  # Общее количество вакансий
    df2['rate'] = df2.groupby('area_name')['area_name'].transform(lambda x: x.count() / count * 100).round(2).astype(float)
    df_by_city_rate = df2.groupby('area_name').agg({
        'rate': 'first'
    }).reset_index() # Группируем DataFrame по названию города и агрегируем значения, выбирая первое значение 'rate'
    df_by_city_rate.columns = ['Город', 'Доля вакансий, %']
    df_by_city_rate = df_by_city_rate.sort_values(by='Доля вакансий, %', ascending=False).reset_index().drop('index', axis=1).head(20)
    creating_tables(df_by_city_rate.to_html(index=False))
    creating_plot(df_by_city_rate.sort_values(by='Доля вакансий, %', ascending=True))

if __name__ == '__main__':
    main()
