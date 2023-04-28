import requests
from bs4 import BeautifulSoup as bs
import json


def get_data():

    URL = "https://api.naturasiberica.ru/api/v1/stores?city=1"
    response = requests.get(URL)

    if response.status_code != 200:
        print('Error')

    result_list = []

    results = response.json()['data']
    data_store = results.get('list')

    for info in data_store:

        '''address'''
        address = info.get('address')

        '''coordinates'''
        latitude = info.get('latitude')
        longitude = info.get('longitude')
        coords = [latitude, longitude]

        '''name'''
        name = info.get('name')

        '''phone'''
        phone = info.get('phone')

        '''working hours'''
        working_hours = info.get('schedule')

        '''adding data to the lapse list'''
        lapse_result = {
            "address": address,
            "latlon": coords,
            "name": name,
            "phones": phone,
            "working_hours": working_hours
        }
        result_list.append(lapse_result)

    with open('natura.json', 'w', encoding='utf-8') as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
