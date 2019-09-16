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
from helper import get_div_text, get_div_block
from wrapper import Wrapper

class SteamWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = {}
        # details
        details = soup.find_all("div", class_="details_block")
        if details:
            for d in details:
                if "Title" in d.get_text():
                    template['details'] = get_div_block(d)
                    break
        # price
        #price = soup.find("div", class_="discount_original_price")
        #if price:
        #    template['price'] = price.get_text()
        # Requirements min
        reqs_min = soup.find("div", class_="game_area_sys_req_leftCol")
        if reqs_min:
            template['Req_min'] = get_div_text(list(reqs_min.children)[1])
        # Requirements max
        reqs_max = soup.find("div", class_="game_area_sys_req_rightCol")
        if reqs_max:
            template['Req_max'] = get_div_text(list(reqs_max.children)[1])
        # About this game
        description = soup.find_all("div", class_="game_area_description")
        if description:
            template['description'] = get_div_text(description[1])

        return template
