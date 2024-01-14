import json
import re

import requests
from bs4 import BeautifulSoup

from . import query
from .utils import HEADERS, parse_naver_var_in_script_texts


class PlaceMixin:
    def search_places(self, keyword: str, page_no: int, page_size: int, proxies=None):
        data = query.get_restaurants.create(keyword, page_no, page_size)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']['restaurants']
        return graphql_data

    def get_place(self, business_id, proxies=None):
        # url = f"https://pcmap.place.naver.com/restaurant/{business_id}/home"
        url = "https://pcmap.place.naver.com/restaurant/{}".format(business_id)
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        html_text = response.content

        broadcasts = self.__parse_broadcast_in_html(html_text)
        return broadcasts

    def get_restaurant(self, business_id, proxies):
        data = query.get_restaurant.create(business_id)
        response = requests.post("https://pcmap-api.place.naver.com/graphql", headers=HEADERS, data=json.dumps(data),
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        graphql_data = response_data['data']
        return graphql_data

    def __parse_broadcast_in_html(self, html_text: str):
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)
        variable_name = 'window.__APOLLO_STATE__'
        pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
        match = pattern.search(naver_var)

        if match:
            data = match.group(1)
            return json.loads(data[:-1])
        else:
            return None

    def get_place_summary(self, id: str, proxies=None):
        url = f"https://map.naver.com/v5/api/sites/summary/" + id + "?lang=ko"
        data = {
            "language": 'kor',
            "order_by": "2"
        }
        response = requests.get(url, data=data, proxies=proxies)
        response.raise_for_status()
        resposne_data = response.json()
        resposne_data['_id'] = id
        return resposne_data

    def get_menus(self, business_id, proxies=None):
        url = f"https://pcmap.place.naver.com/restaurant/{business_id}/menu/list"
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        html_text = response.content
        menus = self.__parse_menus_internal(html_text)
        result = {
            "business_id": business_id,
            "menus": menus
        }
        return result

    def __parse_menus_internal(self, html_text: str):
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")
        naver_string = None

        for s in scripts:
            if s.string is None:
                continue
            if "var naver=" in s.string:
                naver_string = s.string

        menu_regex = re.compile(r'\{"__typename":"Menu".*?\}')
        menu_string_list = re.findall(menu_regex, naver_string)

        # 일반
        menus = []
        for menu_string in menu_string_list:
            menu_json = json.loads(menu_string)
            menu = {
                "name": menu_json["name"],
                "price": menu_json["price"],
                "description": menu_json["description"],
                "imageUrl": menu_json["images"][0] if menu_json["images"] else "",
                "isRecommended": menu_json["recommend"],
            }
            menus.append(menu)
        # baemin
        baemin_menu_regex = re.compile(r'\{"__typename":"BaeminMenu".*?\}')
        baemin_menu_string_list = re.findall(baemin_menu_regex, naver_string)

        for baemin_menu_string in baemin_menu_string_list:
            baemin_menu_json = json.loads(baemin_menu_string)
            menu = {
                "name": baemin_menu_json["name"],
                "price": baemin_menu_json["price"],
                "imageUrl": menu_json["images"][0] if menu_json["images"] else "",

            }
            menus.append(menu)
        return menus

    def search_keyword_in_html_in_first_page(self, keyword, x=None, y=None, bounds=None, proxies=None):
        url = "https://pcmap.place.naver.com/restaurant/list?query={}".format(keyword)
        # url = 'https://map.naver.com/v5/search/'
        response = requests.get(url,
                                params={
                                    x: x,
                                    y: y,
                                    bounds: bounds
                                },
                                proxies=proxies)
        response.raise_for_status()
        html_text = response.content
        soup = BeautifulSoup(html_text, "html.parser", from_encoding="utf-8")
        scripts = soup.find_all("script")

        naver_var = parse_naver_var_in_script_texts(scripts)
        variable_name = 'window.__APOLLO_STATE__'
        pattern = re.compile(rf'\b{re.escape(variable_name)}\s*=\s*(.*?)(\n)')
        match = pattern.search(naver_var)

        if match is None:
            return None

        data = match.group(1)
        json_data = json.loads(data[:-1])

        return json_data
    #
    #
    # def search_keyword_in_bound(self, keyword, x, y, bound):
