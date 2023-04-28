import requests
from bs4 import BeautifulSoup as bs
import lxml
import json
import re


def get_data():

    URL = "https://oriencoop.cl/sucursales.htm"
    response = requests.get(URL)

    if response.status_code != 200:
        print('Error')

    html = bs(response.text, 'html.parser')
    body = html.find('div', 'c-left').find('ul', 'c-list c-accordion')
    el = body.find_all('ul', 'sub-menu')
    result_list = []

    for item in el:
        cont = item.find_all('a')
        for i in cont:
            '''open the brunch page'''
            temp_url = 'https://oriencoop.cl' + i.get('href')
            r = requests.get(temp_url)
            html_info = bs(r.text, 'html.parser')
            info = html_info.find('div', 'c-right').find('div', 'sucursal')
            info_list = info.find_all('p')

            '''name'''
            name = info.find('h3')

            '''address'''
            address = info_list[0].find('span')

            '''phone'''
            phone = info_list[1].find('span')

            '''working hours'''
            hours = info_list[3].find_all('span')
            working_hours = [hours[0].text, hours[1].text]

            '''coordinates'''
            coords_url = info.find('iframe').attrs['src']
            coords_regex = r"2d(-?\d+\.\d+)!3d(-?\d+\.\d+)!"
            match = re.search(coords_regex, coords_url)
            coordinates = []
            if match:
                coordinates.append(match.group(1))
                coordinates.append(match.group(2))

            '''adding data to the lapse list'''
            lapse_result = {
                "address": address.text,
                "latlon": coordinates,
                "name": name.text,
                "phones": phone.text,
                "working_hours": working_hours
            }
            result_list.append(lapse_result)

        with open('oriencoop.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()
