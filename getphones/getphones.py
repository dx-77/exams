#!/usr/bin/env python3
#
#Скрипт для поиска телефонных номеров (российских мобильных или московских стационарных) на web страницах
#A script for searching russian phone numbers in web pages
# Format to search 
#[+7]|[7]|[8][ (][9хх|495|498|499|800][) ][ххх[_|-]хх[_|-]хх | ххх[_|-]х[_|-]xхх|xx[_|-]xx[_|-]xxx|xx[_|-]xxx[_|-]xx]
#_xxx[_|-]xx[_|-]xx_
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
import json
import re
import threading
import time
from bs4 import BeautifulSoup
import requests

TEST = False

PROGRAM_VER = 'GetPhones version 0.91'

USERAGENT = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0)'
             ' Gecko/20100101 Firefox/58.0'}

PHONESFILE = 'phones.txt'
URLSFILE = 'urls.txt'

EXPR = (r'(?:[^0-9+(]|\b|^)((?:\+7|8|7)?(?:\(|[ ]| \()?(?:9[0-9]{2}|495|498|499|800)'
        r'(?:\)|[ ]?|\) )?(?:[0-9]{3}[- ]?(?:[0-9]{2}[- ]?[0-9]{2}|[0-9][- ]?[0-9]{3})|'
        r'(?:[0-9]{2}[- ]?[0-9]{2}[- ]?[0-9]{3}|[0-9]{2}[- ]?[0-9]{3}[- ]?[0-9]{2}))|'
        r'(?:(?:\s|^)[0-9]{3}[- ]?[0-9]{2}[- ]?[0-9]{2}(?:\s|$)))(?:\D|\b|$)'
    )

PAGES = [
    'https://hands.ru/company/about',
    'http://wizardom.ru/контакты/',
    'http://dom-helper.ru/contacts/',
    'http://www.telemaster-msk.ru/kontakti.html',
    'http://m-econom.ru/наши-контакты',
    'http://kvadr-remont.ru/kontaktyi/',
    'http://help-kar.ru/address',
    'http://www.remontelektroniki.ru/contact-us/',
    'http://1rbt.ru/',
    'http://www.remontexpress.ru/contacts/',
    'http://stroi-otdelka.ru/contact/',
    'https://www.dommaster.su/contacts',
    'http://masterbosch.ru/contacts/',
    'http://www.bitpribor.ru/'
]


def bench(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        func(*args, **kwargs)
        t = time.time() - now
        min = t // 60
        sec = t - min * 60
        print('%s- %0.2f min. %0.2f sec.' % (func.__name__, min, sec))
    return wrapper


def format_phones(phones):
    for i in range(len(phones)):
        res = re.findall(r'\d', phones[i])

        if len(res) == 11:
            if res[0] == '8' and res[1] != '8' or res[0] == '7':
                res[0] = '+7'
        elif len(res) == 7:
             res = [' '] * 4 + res
        elif len(res) == 10:
            res = ['+7'] + res
        else:
            print('Something wrong with phone number !!!')

        phone = res[0] + ' ' + res[1] + res[2] + res[3] + ' ' + res[4] + res[5] +\
                res[6] + ' ' + res[7] + res[8] + ' ' +  res[9] + res[10]
        phones[i] = phone.lstrip()

    phones = list(set(phones))
    phones.sort()
    return phones


class Parser(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        
    def run(self):
        global results

        try:
            url = self.url
            page = requests.get(url, headers=USERAGENT).text
                       
            soup = BeautifulSoup(page, 'html.parser')

            if not TEST:
                tags = soup.find_all(class_=re.compile(r'phone|tel|description|contact')) or []
            else:
                tags = soup.find_all(class_=re.compile(r'phone|tel|description|contact|blob')) or []

            tags = tags + (soup.find_all('p') or [])
                      
            if tags:
                results[url] = results.get(url, [])
                for t in tags:
                    text = t.get_text()
                    text = text.replace('\xa0', ' ')
                    res = re.findall(EXPR, text)
                    if res:
                        results[url].extend(res)
        
                results[url] = format_phones(results[url])

        except Exception as e:
            print('Unable to open "%s"' % url)
            print(e)

@bench
def find_phones(urls, save=True, filename=PHONESFILE):
    if not urls: return

    global results

    results = {}
    if save and not TEST:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                results = json.load(f)
        except:
            pass
    
    threadsnumber = len(threading.enumerate())
    i = -1
    all_parsed = False
    while not all_parsed:
        while True:
            i += 1
            url = urls[i]
            if url:
                parser = Parser(url)
                parser.start()
            if i == len(urls) - 1:
                all_parsed = True
                break
            if not i % 150:
                break
       
        threads = str(threading.enumerate())
        if threads.find('Parser') != -1:
            while len(threading.enumerate()) > threadsnumber:
                pass
        else:
            print('Something wrong!!!!!')
            break
  
    if not save:
        for url in set(urls):
            print('\n%s - %d номер(а,ов)' % (url, len(results[url])))
            
            for phone in results[url]:
                print('    %s' % phone)
            print()

    else:
        try:
            if len(urls) <= 100:
                for url in set(urls):
                    print('\n%s - %d номер(а,ов)' % (url, len(results[url])))
            else:
                print('Обработано %d url' % len(urls))
               
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, sort_keys=True, indent=4)
            print('Телефоны успешно сохранены в файле "%s"' % filename)
        except Exception as e:
            print('Unable to save to file "%s"' % filename)
            print(e)


def load_urls(filename=URLSFILE):
    try:
        with open(filename, encoding='utf-8') as f:
            urls = f.read().strip()
    except Exception as e:
        print('Cannot read from "%s"' % filename)
        print(e)
        return
    urls = urls.replace('\ufeff', '')
    urls = urls.splitlines()
    return urls
 

if __name__ == '__main__':
    print(PROGRAM_VER)

    if TEST:
        print('Start tests...')
        print('\nTest0')
        text = ('7777777 89999251254asdas 123-45-67 (695)458712 +7 923 125 25-48;'
               'к/c 4545488000000000154 892364435-87 1234568'
               ' 929 15-111-25 master-5074636@yandex.ru')
        print(text)
        print('Probably phone numbers:%s' % re.findall(EXPR, text))
        
        print('\nTest1')
        print("""
            Output must be
            https://yandex.ru/company/contacts/moscow/ - 8 номер(а,ов)
            +7 495 739 23 32
            +7 495 739 37 77
            +7 495 739 70 00
            +7 495 739 70 70
            +7 495 974 35 81
            8 800 234 24 80
            8 800 250 66 99
            8 800 250 96 39
            https://rambler-co.ru/contacts - 1 номер(а,ов)
            +7 495 785 17 00\n\n
        """)
        find_phones(['https://yandex.ru/company/contacts/moscow/', 'https://rambler-co.ru/contacts'], save=False)

        print('\nTest2')
        print('must be 28342 phones')
        find_phones(['https://github.com/dx-77/getphones/blob/master/phones.htm'], filename='test.txt') 

        print('\nTest3')
        print('load testing- parsing speed <= 1 min 10 sec. on (core i3 ivy bridge)')
        find_phones(PAGES*70, save=False) 
       
    while not TEST:
        print('\n1. Найти и показать на экране номера телефонов') 
        print('2. Найти и сохранить в файле найденные номера телефонов') 
        print('3. Выйти из программы') 
        num = input('Введите номер пункта меню (1, 2, 3) и нажмите Enter: ') 
        if num == '1':
            print('Searching...')
            find_phones(load_urls(), save=False)
        elif num == '2':
            print('Searching...')
            find_phones(load_urls())
        elif num == '3':
            break
        else:
            print('Такой пункт меню отсутствует!')