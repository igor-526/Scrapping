import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers
from datetime import datetime


def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()


def get_urls():
    urls = []
    response = requests.get('https://spb.hh.ru/vacancy/76779932?from=vacancy_search_list&query=python',
                            headers=get_headers())
    soup = BeautifulSoup(response.text, features='lxml')
    titles = soup.find_all(class_='serp-item__title')
    for title in titles:
        urls.append(title['href'])
    return urls


def writejson(data):
    currenttime = datetime.now()
    name = f'{currenttime.strftime("%d.%m-%H.%M")}.json'
    with open(name, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    print(f'Подробности записаны в файл {name}')


if __name__ == "__main__":
    data = {}
    for url in get_urls():
        response = requests.get(url, headers=get_headers())
        soup = BeautifulSoup(response.text, features='lxml')
        description = soup.find(class_='vacancy-description').text
        if "django" in description or "linux" in description.lower():
            title = soup.find(class_='bloko-header-section-1').text
            company = soup.find(class_='vacancy-company-details').text
            salary = soup.find(class_='bloko-header-section-2 bloko-header-section-2_lite').text
            data[title] = {'company': company, 'salary': salary, 'url': url}
            print(f'{title}: {salary}')
    writejson(data)
