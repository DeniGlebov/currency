from time import sleep
import random
from fake_useragent import UserAgent

import requests
from bs4 import BeautifulSoup

from datetime import datetime
import locale
import sqlite3

conn = sqlite3.connect("workua.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE workua
                  (date_vacancy text, 
                  name_vacancy text, 
                  salary text, 
                  company_name text, 
                  company_type text, 
                  company_address text, 
                  vacancy_text text, 
                  url_vacancy text)
               """)
conn.commit()
conn.close()


def random_sleep():
    sleep(random.randint(1, 3))


BASE_URL = 'https://www.work.ua/ru/jobs/'
ua = UserAgent()

with open('workua.txt', 'w') as file:
    page = 0

    while True:
        page += 1
        print(f'start to parse page: {page}')

        headers = {'User-Agent': ua.random}

        response = requests.get(BASE_URL, params={'page': page}, headers=headers)
        response.raise_for_status()
        random_sleep()

        soup = BeautifulSoup(response.text, 'html.parser')

        res = soup.find('div', {'id': 'pjax-job-list'})

        if res is None:
            break

        res = res.find_all('h2')
        for elem in res:
            href = elem.find('a').attrs['href']
            file.write(f'{href}\n')

BASE_URL_VACANCY = 'https://www.work.ua'
with open('workua.txt', 'r') as file:
    for x in file:
        url_vacancy = f'{BASE_URL_VACANCY}{x}'.replace(u'\n', u'')
        print(url_vacancy)
        headers = {'User-Agent': ua.random}

        locale.setlocale(locale.LC_ALL, "ru_RU")
        today = datetime.today().strftime("%d %B %Y")
        response = requests.get(url_vacancy, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        vacancy = soup.find('div', {'class': 'card wordwrap'})

        date_vacancy = ''
        salary = ''
        name_vacancy = ''
        company_name = ''
        company_type = ''
        company_address = ''
        vacancy_text = ''

        if vacancy:
            if vacancy.findAll('span', {'class': 'label label-hot'}):
                date_vacancy = f'Вакансия от {today}'
            else:
                date_vacancy = vacancy.findAll('span', {'class': 'text-muted'})[0].text.replace(u'\xa0', u' ')

            if vacancy.findAll('span', {'class': 'glyphicon glyphicon-hryvnia text-black glyphicon-large'}):
                salary = vacancy.find('p', {'class': 'text-indent text-muted add-top-sm'}).text.strip().replace(
                    u'\u202f', u' ').replace(u'\u2009', u' ').replace(u'\xa0', u' ')
            else:
                salary = 'Скрыто'

            if vacancy.findAll('h1', {'class': 'add-top-sm'}):
                name_vacancy = vacancy.findAll('h1', {'class': 'add-top-sm'})[0].text

            if vacancy.findAll('p', {'class': 'text-indent text-muted add-top-sm'}):
                if vacancy.findAll('p', {'class': 'text-indent text-muted add-top-sm'})[-1].find('b'):
                    company_name = vacancy.findAll('p', {'class': 'text-indent text-muted add-top-sm'})[-1].find(
                        'b').text
                else:
                    company_name = vacancy.findAll('p', {'class': 'text-indent text-muted add-top-sm'})[
                        -1].text.strip().replace('  ', '').replace(u'\n', u' ')

            if vacancy.findAll('span', {'class': 'add-top-xs'}):
                company_type = vacancy.findAll('span', {'class': 'add-top-xs'})[0].text.strip().replace(
                    '  ', '').replace(u'\xa0', u' ').replace(u'\n', u' ')
            else:
                company_type = 'Скрыто'

            if vacancy.findAll('p', {'class': 'text-indent add-top-sm'}):
                company_address = vacancy.findAll('p', {'class': 'text-indent add-top-sm'})[0].text.strip().replace(
                    '  ', '').replace(u'\xa0', u' ').replace(u'\n', u' ').replace(u' ·  На карте', u'')

            if vacancy.findAll('p', {'class': 'text-indent add-top-sm'}):
                conditions = vacancy.findAll('p', {'class': 'text-indent add-top-sm'})[-1].text.strip().replace(
                    '  ', '').replace(u'\n', u' ')

            if vacancy.findAll('div', {'id': 'job-description'}):
                vacancy_text = vacancy.findAll('div', {'id': 'job-description'})[0].text.strip().replace(
                    '  ', '').replace(u'\n', u' ')

            conn = sqlite3.connect("workua.db")
            cursor = conn.cursor()

            params = (
                date_vacancy,
                name_vacancy,
                salary,
                company_name,
                company_type,
                company_address,
                vacancy_text,
                url_vacancy)

            conn.execute("INSERT INTO workua VALUES (?, ?, ?, ?, ?, ?, ?, ?)", params)
            conn.commit()
            conn.close()
        else:
            continue
