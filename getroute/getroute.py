#!/usr/bin/env python3
#
# Скрипт для определения маршрута движения автомобиля между N ≤ 4 точек. 
# Входная информация (наименования городов\населенных пунктов), вывод должен содержать:
# координаты всех внесенных точек;
# дистанцию на маршруте в км;
# ориентировочное время в пути;
#
# A script for seartching car route between <=4 localities
#
# Copyright (C) 2018 dx-77 <d.x77@yandex.ru>.
# GitHub : https://github.com/dx-77
#
# This program is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import googlemaps
import requests

ROUTE_URL = 'https://maps.googleapis.com/maps/api/directions/json'

KEY = 'AIzaSyDQ033vdji13ejN4lzFEB1NN8HLg8-1HTA'

params = {'mode': 'driving',
          'origin': '',
          'waypoints': '',
          'destination': '',
          'key': KEY}


def getcoords(locality):
    coords = []
    f_addresses = []

    for l in locality:
        gr = gmaps.geocode(l)
        if gr:
            f_addresses.append(gr[0]['formatted_address'])
            lng = gr[0]['geometry']['location']['lng']
            lat = gr[0]['geometry']['location']['lat']
            coords.append(str(lng) + ',' + str(lat))

    return [f_addresses, coords]


if __name__ == '__main__':
    gmaps = googlemaps.Client(key=KEY)
    
    while True:
        print('Please input 2-4 localities (Enter for none)')
        A = input('locality A: ').strip()
        WP1 = input('Waypoint: ').strip()
        WP2 = input('Waypoint: ').strip()
        B = input('locality B: ').strip()
        locality = [i for i in (A, WP1, WP2, B) if i]
        if A and B:
            break
        print('\nInput at A and B!\n')

    f_addresses, coords = getcoords(locality)
    
    print('Creating the route...')
    for i in range(len(f_addresses)):
        print('"%s" (%s)' % (f_addresses[i], coords[i]))
       
    params['origin'] = f_addresses[0]
    params['destination'] = f_addresses[-1]

    if WP1 and WP2:
        WP1 = f_addresses[1] + '|via:' + f_addresses[2]
    elif WP2:
        WP1 = f_addresses[1]
    if WP1:
        params['waypoints'] = 'via:' + WP1
    
    res = requests.get(ROUTE_URL, params=params)
    if res.status_code == requests.codes.ok:
        res = res.json()
        print(res['routes'][0]['legs'][0]['distance']['text'])
        print(res['routes'][0]['legs'][0]['duration']['text'])
    else:
        print('Cannot open URL %s' % ROUTE_URL)
