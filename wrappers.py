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
from helper import get_div_text, get_div_dict, get_meta_dict
from wrapper import Wrapper, game_template

class SteamWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template
        # details
        details = soup.find_all("div", class_="details_block")
        if details:
            for d in details:
                if "Title" in d.get_text():
                    tmp = get_div_dict(d)
                    template['title'] = tmp['Title:'][0]
                    template['genre'] = tmp['Genre:']
                    break

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


class NuuvemWrapper(Wrapper):

    def __init__(self):
        pass


    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template

        # meta tags
        meta_tags = soup.find_all("meta")
        meta_dict = get_meta_dict(meta_tags)

        # title
        if 'name' in meta_dict:
            template['title'] = meta_dict['name'][0]

        # genre
        if 'genre' in meta_dict:
            template['genre'] = meta_dict['genre'][0]

        # reqs_min and max
        requirements = soup.find_all("div", class_="product-system-requirements--item--content")

        if requirements and len(requirements) == 2:
            template['Req_min'] = get_div_text(requirements[0])
            template['Req_max'] = get_div_text(requirements[1])

        # About this game
        description = soup.find_all("div", class_="product-content--text product-content--text__read-more")[0]
        if description:
            template['description'] = description.get_text()

        return template
