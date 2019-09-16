"""
Wrappers especificos para cada site:

Steam
Humble Bundle
Epic Games
Gamesdeal
Ubisoft
GOG
Nuuvem
Winstore
Amazon Games
Xbox Store
"""
from bs4 import BeautifulSoup
from helper import get_div_text
from wrapper import Wrapper

lista = ["About This Game", "Reviews"]

class SteamWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = {}
        # price
        price = soup.find("div", class_="discount_original_price")
        if price:
            template['price'] = price.get_text()
        # Requirements min
        reqs_min = soup.find("div", class_="game_area_sys_req_leftCol")
        if reqs_min:
            template['Req_min'] = get_div_text(list(reqs_min.children)[1])
        # Requirements max
        reqs_max = soup.find("div", class_="game_area_sys_req_rightCol")
        if reqs_max:
            template['Req_max'] = get_div_text(list(reqs_max.children)[1])
        # About this game and reviews
        description = soup.find_all("div", class_="game_area_description")
        if description:
            template['description'] = get_div_text(description[1])
            template['review'] = get_div_text(description[0])

        return template
