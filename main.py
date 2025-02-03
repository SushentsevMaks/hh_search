import time

import requests
from bs4 import BeautifulSoup
import telebot

from env import telega_token

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url_perm = "https://perm.hh.ru/search/vacancy?text=FastAPI&salary=&ored_clusters=true&area=72&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line"

url_rf = "https://perm.hh.ru/search/vacancy?ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&schedule=remote&area=113&experience=between1And3&text=FastAPI"

def search_vac(headers, url):
    src = requests.get(url, headers=headers).text
    soup = BeautifulSoup(src, 'html.parser')
    vacancies = soup.find_all('a', {'data-qa': 'serp-item__title'})

    vac = {}

    for vacancy in vacancies:
        title = vacancy.find('span', {'data-qa': 'serp-item__title-text'}).text
        link = vacancy['href']
        vac[link] = title


    with open("vacancies.txt", "r+", encoding="UTF-8") as file:
        old_vac = [i.strip() for i in file.readlines()]
        for link in vac.keys():
            if link not in old_vac:
                chat_id = -695765690
                bot = telebot.TeleBot(telega_token)
                message = (f"Новая вакансия - {vac[link]}"
                           f"\n"
                           f"{link}")
                bot.send_message(chat_id, message)
                file.write(link + "\n")
                time.sleep(1)


while True:
    search_vac(headers, url_perm)
    search_vac(headers, url_rf)
    time.sleep(42000)
