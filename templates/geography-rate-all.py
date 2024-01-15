import matplotlib.pyplot as plt    
import pandas as pd


def creating_tables(table):
    f1 = open(f"geography/tables/top_20_cities_by_rate.html", "w", encoding='utf-8')
    f1.write(table)
    f1.close()
    return


def creating_plot(df):
    plt.figure(figsize=(16, 8))
    plt.barh(df['Город'], df['Доля вакансий, %'])
    plt.tick_params(axis='y', labelrotation=0, labelsize=15)
    plt.tick_params(axis='y', labelright=False, labelleft=True)
    plt.tick_params(axis='x', labelrotation=0, labelsize=15)
    plt.title('Доля вакансий по городам', fontdict = {'fontsize' : 24})
    plt.tight_layout()
    plt.savefig(f"geography/graphs/graph_top_20_cities_by_rate.png", dpi=100)
    return


def main():
    df2 = pd.read_csv("vacancies.csv", usecols=['area_name', 'published_at'])
    count = len(df2)
    df2['rate'] = df2.groupby('area_name')['area_name'].transform(lambda x: x.count() / count * 100).round(2).astype(float)
    df_by_city_rate = df2.groupby('area_name').agg({
        'rate': 'first'
    }).reset_index()
    df_by_city_rate.columns = ['Город', 'Доля вакансий, %']
    df_by_city_rate = df_by_city_rate.sort_values(by='Доля вакансий, %', ascending=False).reset_index().drop('index', axis=1).head(20)
    creating_tables(df_by_city_rate.to_html(index=False))
    creating_plot(df_by_city_rate.sort_values(by='Доля вакансий, %', ascending=True))


if __name__ == '__main__':
    main()