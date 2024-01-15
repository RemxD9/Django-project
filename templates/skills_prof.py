import pandas as pd
import matplotlib.pyplot as plt


def main():
    # Считываем данные, используя только необходимые столбцы
    data = pd.read_csv("vacancies.csv", usecols=['name', 'key_skills', 'published_at'])
    data.dropna(subset=['name', 'key_skills'])
    selected_profession = 'Devops-инженер'
    data = data[data['name'].str.contains(selected_profession, na=False, case=False)]
    data['published_at'] = pd.to_datetime(data['published_at'], utc=True).dt.year
    years_list = sorted(data['published_at'].unique())
    creating_skills_for_years(data, years_list)
    return


def creating_skills_for_years(data, years_list):
    for year in years_list:
        years_skills_list = (data[data['published_at'] == year]['key_skills'].str.split(',|\n',
                                                                                        expand=True).stack()
                                .value_counts().nlargest(20))
        if years_skills_list.size == 0:
            continue
        top_skills = pd.DataFrame({'Навык': years_skills_list.index, 'Количество': years_skills_list.values})
        creating_plot(top_skills, str(year))
        creating_html_tables(str(year), top_skills.to_html(index=False))
    return


def creating_plot(df, year):
    fig, ax = plt.subplots()
    bars = ax.barh(df['Навык'], df['Количество'])
    ax.tick_params(axis='y', labelrotation=0, labelsize=8)
    ax.tick_params(axis='y', labelright=False, labelleft=True)
    plt.title(year)
    plt.tight_layout()
    plt.savefig(f"skills/graphs/graph_prof_top_20_by_{year}.png")
    return


def creating_html_tables(year, table):
    f1 = open(f"skills/tables/prof_top_20_by_{year}.html", "w", encoding='utf-8')
    f1.write(table)
    f1.close()
    return


if __name__ == '__main__':
    main()
