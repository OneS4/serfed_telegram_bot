import requests
from bs4 import BeautifulSoup


# noinspection PyBroadException
def find_weather(city):
    try:
        html_doc = requests.get(f'https://www.gismeteo.ru/weather-{city}/2-weeks/', headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}).text
        soap = BeautifulSoup(html_doc, 'lxml')
        body = soap.find('div', class_='widget-items')
        days = list()
        for elem in body.find(class_='widget-row widget-row-days-date').find_all(class_='row-item'):
            date = ''
            day = elem.find_all('div')
            for char in day[1].text:
                if char != ' ' and char != '\n':
                    date += char
            days.append(f'{day[0].text} {date}')
        weather = list()
        for elem in body.find(class_='widget-row widget-row-icon').find_all(class_='weather-icon tooltip'):
            weather.append(elem.get('data-text'))
        temperature_day = list()
        temperature_night = list()
        for i, elem in enumerate(body.find_all(class_='unit unit_temperature_c')):
            if i % 2 == 0:
                temperature_day.append(elem.text)
            else:
                temperature_night.append(elem.text)
        return {'days': days, 'weather': weather, 'temperature_day': temperature_day,
                'temperature_night': temperature_night}
    except:
        return False
