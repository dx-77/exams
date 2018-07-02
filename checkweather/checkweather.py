#!/usr/bin/env python3
#
#Скрипт оценки достоверности дневного прогноза погоды в Москве сервиса Яндекс.Погода по сроку предсказания
#A script for assessing the reliability of the weather forecast in Moscow by Yandex.Weather on the date of prediction
#
#Copyright (C) 2018 dx-77 <d.x77@yandex.ru>.
#GitHub : https://github.com/dx-77
#
#This program is free software: you can redistribute it and/or modify it under the terms
#of the GNU General Public License as published by the Free Software Foundation,
#either version 3 of the License, or (at your option) any later version.
#This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#See the GNU General Public License for more details.
# 
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from datetime import datetime, timedelta
import json
import urllib.request
from bs4 import BeautifulSoup

CITY = 'moscow'
WEATHER_URL = 'https://yandex.ru/pogoda/'
MAX_DAYS = 7
# Current Yandex Tags 16.06.2018
FACT_TEMP_TAG = 'temp fact__temp'
NOW_DATE_TAG = 'datetime' #'<time class="time fact__time" datetime="'
LOCATION_TAG = 'location'  # h1
FORECAST_DATE_TAG = 'time forecast-briefly__date'
FORECAST_TEMP_TAG = 'forecast-briefly__temp_day'


def save_weather(soup, now, filename):
    filename = filename + '.txt'
    now = now.split() # now consists [0] - 'date' and [1] - 'time'
    weather_list = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            weather_list = json.load(f)
    except:
        pass
   
    try:
        weather_list[now[0]] = {'fc_time':now[1], 'forecast':{}}
       
        days = soup.find_all(class_=FORECAST_DATE_TAG)
        days = days[1:MAX_DAYS + 1]
        temps = soup.find_all(class_=FORECAST_TEMP_TAG)
        temps = temps[1:MAX_DAYS + 1]

        for i in range(MAX_DAYS):
            day = days[i]['datetime'].split()[0]
            temp = temps[i].get_text()[:-1]
            weather_list[now[0]]['forecast'][day] = temp
        
    except Exception as e:
        print('Probably HTML has been modified!')
        print(e)
        return

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(weather_list, f, sort_keys=True, indent=4)
        print('Прогноз успешно сохранен в файле "%s"' % filename)
    except Exception as e:
        print('Unable to save to file "%s"' % filename)
        print(e)
    

def load_weather(now, filename, now_temp, days_to_load):
    if days_to_load > MAX_DAYS: days_to_load = MAX_DAYS
    filename = filename + '.txt'
    now = now.split()[0] # now consists 'date'
    date = datetime.strptime(now, "%Y-%m-%d")
    dates_to_check = []
    for i in range(1, days_to_load + 1):
        d = date + timedelta(days=-i)
        dates_to_check.append(datetime.strftime(d, "%Y-%m-%d"))

    weather_list, forecast_temp = {}, []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            weather_list = json.load(f)
        
        for dtc in dates_to_check:
            if dtc in weather_list:
                if now in weather_list[dtc]['forecast']:
                    forecast_temp.append((dtc, weather_list[dtc]['forecast'][now]))

        if forecast_temp == []:
            print('Файл "%s" не содержит прогнозов на дату %s' % (filename, now.split()[0]))
            return
            
        now_temp = float(now_temp)
        for ft in forecast_temp:
            fc_temp = float(ft[1])
            if fc_temp:
                percent = now_temp*100/fc_temp - 100
            else:
                percent = 999
            print(
                'Сегодняшняя погода отличается от предсказанной %s  на %0.1f%% (%0.1f°)' \
                % (ft[0], percent, now_temp-fc_temp)
            )
    except Exception as e:
        print('Файл с прогнозами не существует, к нему нет доступа или он имеет неверный формат!'
              'Cannot read the file "%s"' % filename)
        print(e)
       

def estimate(action, days_to_load=MAX_DAYS, url=WEATHER_URL, city=CITY):
    try:
        weather_html = urllib.request.urlopen(url + city).read()
    except Exception as e:
        print('Unable to open page "%s"' % (url + city))
        print(e)
        return
    
    soup = BeautifulSoup(weather_html, 'html.parser')
        
    current_date = soup.time[NOW_DATE_TAG]
    current_temp = soup.find(class_=FACT_TEMP_TAG).get_text()[:-1]
    location = soup.find(class_=LOCATION_TAG).h1.string
    
    if action == 'est':
        print('\nСейчас: %s \n%s: %s°' % (current_date, location, current_temp))
        load_weather(current_date, city, current_temp, days_to_load)
    elif action == 'chk':
        print('\nСейчас: %s \n%s: %s°' % (current_date, location, current_temp))
    elif action == 'sv':
        save_weather(soup, current_date, city)
 

if __name__ == '__main__':
    action = {'1':'est', '2':'chk', '3':'sv'}
    print('CheckWeather version 0.7')
    while True:
        print('\n1. Оценить достоверность прогноза') # Check weather reliability
        print('2. Показать актуальную погоду') # Show actual weather
        print('3. Сохранить сегодняшний прогноз на %d дн.' % MAX_DAYS) # Save weather forecast to file
        print('4. Выход из программы') # Exit program
        num = input('Введите номер пункта меню (1, 2, 3 или 4) и нажмите Enter: ') # Input number
        if num in ('1', '2', '3'):
            estimate(action[num])
        elif num == '4':
            break
        else:
            print('Такой пункт меню отсутствует!') # There is no such number       