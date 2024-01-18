import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup

# Список валют
currencies = ["BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]

# Список столбцов для данных о курсах валют
cols = ["date", "BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]

# Генерация списка дат с января 2003 по декабрь 2023 с шагом в месяц
dates = pd.date_range(start=datetime.datetime(2003, 1, 1), end=datetime.datetime(2023, 12, 1), freq='MS').tolist()

# Преобразование дат в строковый формат
dates_as_string = [date.strftime('%d/%m/%Y') for date in dates]

# Список для хранения данных
data = []

# Итерация по датам
for i in range(len(dates)):
    # Формирование URL для запроса курсов валют на заданную дату
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={dates_as_string[i]}"

    # Отправка запроса
    response = requests.get(url)

    # Парсинг XML-ответа
    soup = BeautifulSoup(response.content, 'xml')

    # Поиск блоков Valute
    valutes = soup.find_all('Valute')

    # Словарь для хранения данных по дате
    date_data = {}

    # Итерация по найденным валютам
    for valute in valutes:
        charcode = valute.CharCode.text
        value = valute.VunitRate.text.replace(',', '.')
        date_data[charcode] = value

    # Формирование строки данных для текущей даты
    row = [dates[i].strftime('%Y-%m')]

    # Добавление значений для каждой валюты
    for currency in currencies:
        if currency in list(date_data.keys()):
            row.append(date_data[currency])
        else:
            row.append(None)

    # Добавление строки данных в общий список
    data.append(row)

# Создание DataFrame из списка данных и сохранение в CSV-файл
df = pd.DataFrame(data, columns=cols)
df.to_csv("currency.csv", index=False)