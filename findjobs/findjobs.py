#!/usr/bin/env python3
#
# Парсер сайта https://www.monster.com/ для сбора описания указанных вакансий
# A script for searching job descriptions on https://www.monster.com/
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
import json
import sys
import textwrap
import threading
import time
from bs4 import BeautifulSoup
import requests

TEST = False

PROGRAM_VER = 'FindJobs version 0.81'

USERAGENT = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0)'
             ' Gecko/20100101 Firefox/58.0'}

JOBSFILE = 'jobs.txt'
URLSFILE = 'urls.txt'
TESTFILE = 'test.py'

PAGES = [
    'https://job-openings.monster.com/Advisory-Financial-Services-Oracle-'
    'Accounts-Payable-Senior-Associate-New-York-NY-US-PWC/22/c6e97461-efec-40e2-a6b4-77bb4330a271',

    'https://job-openings.monster.com/Full-Stack-Developer-Python-Django-'
    'ReactJS-Kansas-City-MO-US-CyberCoders/11/197194932',

    'https://job-openings.monster.com/Python-Developer-Jersey-City-NJ-US-Data-Inc/11/197367825',

    'https://stellenangebot.monster.de/IT-Support-Engineer-Managed-Services-Cyber-Security-'
    'Reston-VA-US-CyberCoders/11/197435614?LogGetJobChannelID=10005',

    'https://stellenangebot.monster.de/Federal-Account-Executive-IT-Services-Work-From-Home'
    '-Washington-DC-US-CyberCoders/11/197435813?LogGetJobChannelID=10005',

    'https://stellenangebot.monster.de/Python-Software-Developer-New-Jersey-NJ-US-'
    'Spherion/11/197436380?LogGetJobChannelID=10005',

    'https://job-openings.monster.com/Quant-Python-Developer-Washington-DC-US-The-'
    'Oakleaf-Group/22/156988b6-4a2c-4bc2-9f12-5efa1ae68637',

    'https://job-openings.monster.com/Python-AWS-Developer-Lowell-MA-US-InfoVision/11/197431960',

    'https://job-openings.monster.com/Python-Engineer-Sunnyvale-CA-US-Intelliswift-Software/11/197262588',

    'https://job-openings.monster.com/Python-Web-Developer-Durham-NC-US-Randstad-Technologies/11/197340321'
]


USAGE = ('usage: python findjobs.py [-h] [-v] [-s]',
         '                           -p ["inputfilename"] ["outputfilename"]',
         '                           -p ["url"] ["outputfilename"]',
         'On Linux use python3')

HELP = ('positional arguments:',
        '  -p                      parse the urls in "inputfilename" and save data to "outputfilename"',
        '                          by default -p means: -p "%s" "%s"' % (URLSFILE, JOBSFILE),
        '                          -p "url" parse the url and save data to "outputfilename"',
        '\n',
        'optional arguments:',
        '  -h, --help              Show this help message and exit',
        '  -v, --version           Show program version info and exit',
        '  -s                      Show parsing result, if URLs quantity is more than 100- argument is ignored')

ABOUT = ('%s' % PROGRAM_VER,
         'A script for searching job descriptions on https://www.monster.com/')

COMMANDS = {
    0: '',
    1: '-v',
    2: '-h',
    3: '-p',
    4: '-p -s',
    5: '-p "https://job-openings.monster.com/Python-Engineer-Sunnyvale-CA-US-Intelliswift-Software/11/197262588"',
    6: '-p urls.txt result.txt'
}


def bench(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        res = func(*args, **kwargs)
        if res:
            t = time.time() - now
            min = t // 60
            sec = t - min * 60
            print('%s- %0.2f min. %0.2f sec.' % (func.__name__, min, sec))
    return wrapper


class Parser(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
       
    def run(self):
        global results, parsed

        title, datePosted, description = '', '', ''
        try:
            url = self.url
            page = requests.get(url, headers=USERAGENT)
            status = page.status_code
            if status != requests.codes.ok:
                page.raise_for_status()
                
            page = page.text
            soup = BeautifulSoup(page, 'html.parser')
            tag = soup.find(type="application/ld+json")
            if tag:
                try:
                    info = json.loads(tag.get_text())
                    description = info["description"].replace('<br>', '\n')
                    description = description.replace('\xa0', ' ').strip()
                    title = info["title"] + ' at ' + info["hiringOrganization"]["name"] +\
                        '\n' + info["jobLocation"]["address"]["addressLocality"] + ', ' +\
                        info["jobLocation"]["address"]["addressRegion"] + ' ' +\
                        info["jobLocation"]["address"]["postalCode"]
                    datePosted = info["datePosted"]
                except:
                    pass

            tag = soup.find(id="JobDescription")
            if tag:
                description = tag.get_text(separator="\n")
                description = description.replace('\xa0', ' ').strip()
            try:
                if not title:
                    title = soup.find(class_="heading").get_text().strip()
                if not datePosted:
                    datePosted = soup.find(class_="mux-job-summary").get_text()
                    datePosted = datePosted[datePosted.find('Posted\n')+7:]
                    datePosted = datePosted[:datePosted.find('\n')]
            except:
                pass

        except Exception as e:
            print(e)
            return
            
        if description:
            results[url] = {'title': title, 'datePosted': datePosted,
                            'description': description}
            parsed = True


@bench
def find_jobs(urls, filename=JOBSFILE, show=False):
    if not urls:
        return

    global results, parsed
    results, parsed = {}, False

    if not TEST:
        urls = list(set(urls))
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
            if not i % 100:
                break
       
        threads = str(threading.enumerate())
        if threads.find('Parser') != -1:
            while len(threading.enumerate()) > threadsnumber:
                pass
        else:
            print('Something wrong!!!!!')
            break
  
    if not parsed:
        return

    try:
        print('Обработан(о): %d url' % len(urls))
        if show and len(urls) <= 100:
            print('#'*120)
            print()
            for url in urls:
                wr_url = textwrap.fill(url, width=120)
                wr_descr = textwrap.fill(results[url]['description'], width=120)
                print(
                    '%s URL %s\n%s\n\n%s Title %s\n%s\n\n%s Posted date '
                    '%s\n%s\n\n%s About the Job %s\n\n%s' % ('*' * 57,
                    '*' * 57, wr_url, '*' * 56, '*' * 56,
                    results[url]['title'], '*' * 53, '*' * 53,
                    results[url]['datePosted'], '*' * 52, '*' * 52,
                    wr_descr
                ))
                print('#'*120)
                print()
                               
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, sort_keys=True, indent=4)
        print('\nОписания вакансий успешно сохранены в файле "%s"' % filename)
        return True
    except Exception as e:
        print('Unable to save to file "%s"' % filename)
        print(e)


def load_urls(filename=URLSFILE):
    if filename.startswith('http'):
        return [filename]
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
    
    if TEST:
        import os
        if os.name == 'nt':
            PYTHON = 'python'
        else:
            PYTHON = 'python3'

        print(PROGRAM_VER)
        print('Start tests...')
        i = 0
        try:
            if not os.path.exists(TESTFILE):
                with open(sys.argv[0], encoding='utf-8') as f:
                    self_content = f.read()
                self_content = self_content.replace('TEST = True', 'TEST = False')
                with open(TESTFILE, 'w', encoding='utf-8') as f:
                    f.write(self_content)

            for i in range(len(COMMANDS)):
                print('\nTest #%d' % i)
                command = '%s %s %s' % (PYTHON, TESTFILE, COMMANDS[i])
                print('Running "%s"' % command.replace(TESTFILE, sys.argv[0]).strip())
                print('Output:\n')
                os.system(command)

            os.remove(TESTFILE)
        except:
            pass
        print('\nTest #%d' % (i + 1))
        urls = PAGES * 90
        print('Load test- will be processing %d urls' % len(urls))
        find_jobs(urls, show=True)
    else:
        args = sys.argv[1:]
        if args.count('-h') or args.count('--help'):
            for h in HELP:
                print(h)
        elif args.count('-v') or args.count('--version'):
            for a in ABOUT:
                print(a)
        else:
            show = False
            while args.count('-s'):
                show = True
                args.pop(args.index('-s'))

            if not args.count('-p'):
                for u in USAGE:
                    print(u)
                print('FindJobs: error: the following arguments are required: -p')
            else:
                args = args[args.index('-p') + 1:]
                l = len(args)
                if l == 0:
                    find_jobs(load_urls(), show=show)
                elif l == 1:
                    find_jobs(load_urls(args[0]), show=show)
                else:
                    find_jobs(load_urls(args[0]), filename=args[1], show=show)
