import requests
from datetime import datetime


def convert_salary_to_rubles(salary, currency, published_at):
    # Конвертация зарплаты в рубли по курсу Центробанка
    if currency != 'RUR':
        exchange_rate_url = f'https://www.cbr-xml-daily.ru/archive/{published_at.year}/{published_at.month:02d}/{published_at.day:02d}/daily_json.js'
        exchange_rate_response = requests.get(exchange_rate_url)
        exchange_rate_data = exchange_rate_response.json()
        rate = exchange_rate_data['Valute'][currency]['Value']
        salary['from'] = round(salary['from'] * rate, 2) if 'from' in salary else None
        salary['to'] = round(salary['to'] * rate, 2) if 'to' in salary else None
        salary['currency'] = 'RUR'
    return salary


def convert_salary_range_to_rubles(salary_range, currency, published_at):
    if currency != 'RUR':
        exchange_rate_url = f'https://www.cbr-xml-daily.ru/archive/{published_at.year}/{published_at.month:02d}/{published_at.day:02d}/daily_json.js'
        exchange_rate_response = requests.get(exchange_rate_url)
        exchange_rate_data = exchange_rate_response.json()
        rate = exchange_rate_data['Valute'][currency]['Value']
        salary_range['from'] = round(salary_range['from'] * rate, 2)
        salary_range['to'] = round(salary_range['to'] * rate, 2)
        salary_range['currency'] = 'RUR'
    return salary_range
