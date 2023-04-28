import requests
from bs4 import BeautifulSoup as bs
import json
import re


def get_data():

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    URL = "https://som1.ru/shops/"
    response = requests.get(URL, headers=headers)

    if response.status_code != 200:
        print('Error')

    result_list = []
    ids = set()
    cities_containers = bs(response.text, 'html.parser').find_all('div', 'cities-container')

    for container in cities_containers:
        inputs = container.find_all('input')
        for el in inputs:
            ids.add(el.attrs['id'])

    for city_id in ids:
        '''open the page of each city'''
        cookies = {'BITRIX_SM_CITY_ID': city_id}
        r = requests.get(URL, headers=headers, cookies=cookies)

        if r.status_code != 200:
            print('Error')

        html_city = bs(r.text, 'html.parser')
        city_body = html_city.find('div', 'shops-list')
        a_containers = city_body.find_all('a')

        '''coordinates'''
        coordinates = a_containers[0].attrs['onclick']
        coords = coordinates[len('setCenterMap') + 2:-2].split(',')

        '''open the store's information page'''
        temp = a_containers[1]
        temp_url = 'https://som1.ru' + temp.get('href')
        r_shop = requests.get(temp_url, headers=headers, cookies=cookies)
        html_info = bs(r_shop.text, 'html.parser')
        info_body = html_info.find('div', 'page-body').find('div', 'container')
        info_table = html_info.find('table', 'shop-info-table')

        '''name'''
        name = info_body.find('h1')

        table = info_table.find_all('td')

        '''address'''
        address = table[2]

        '''phone'''
        phone = table[5]

        '''working hours'''
        working_hours = table[8]

        '''adding data to the lapse list'''
        lapse_result = {
            "address": address.text,
            "latlon": coords,
            "name": name.text,
            "phones": phone.text,
            "working_hours": working_hours.text
        }
        result_list.append(lapse_result)

    with open('som.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
