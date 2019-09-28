"""
Wrappers especificos para cada site:

Steam               X
Nuuvem              X
Humble Bundle       X
Epic Games          ?
Gamesdeal           X
Ubisoft             X
GOG                 X
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


class GamesDealWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template

        # Title
        title = soup.find("h1")
        if title:
            template['title'] = title.get_text()

        # h2_tags
        h2_tags = soup.find_all("h2")

        if h2_tags:

            for tag in h2_tags:
                # About this game
                if "About This Game" in tag.get_text():
                    p_tag = tag.find_next("p")
                    template['description'] = p_tag.get_text()

                # Req_min
                if "System Requirements" in tag.get_text():
                    ul_tag = tag.find_next("ul")
                    template['Req_min'] = ul_tag.get_text()
                    break

        return template


class HumbleBundleWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template

        # Title
        title = soup.find_all("h1")
        if title:
            template['title'] = title[0].get_text()

        # genre
        genres_list = []

        for span_tag in soup.find_all('span'):

            if span_tag.get('itemprop') == 'genre':
                genres_list.append(span_tag.get_text())

        template['genre'] = " ".join(genres_list)

        # requirements
        reqs_div = soup.find_all("div", class_="js-property-value property-value")
        if reqs_div:
            reqs = reqs_div[-1]
            template['Req_min'] = get_div_text(reqs)

        # About the game
        for meta_tag in soup.find_all("meta"):
            if meta_tag.get("itemprop") == "description":
                template['description'] = meta_tag.get('content')

        # return
        return template


class UbisoftWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template

        # titles
        button_tags = soup.find_all("button")
        if len(button_tags) >= 2:
            template['title'] = button_tags[1].get('title')

        # genre
        #span_tags = soup.find_all("span", class_="product-details-info-name")
        #if span_tags and len(span_tags) >= 4:
        #
        # Req_min
        req_min = soup.find_all('div', class_="section-content requirements-min")
        if req_min:
            template['Req_min'] = req_min[0].get_text()

        # Req_max
        req_max = soup.find_all('div', class_="section-content requirements-rec")
        if req_max:
            template['Req_max'] = req_max[0].get_text()

        # description
        article_tags = soup.find_all('article')
        if article_tags:
            template['description'] = article_tags[0].get_text()

        return template


class GOGWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template

        # title
        h1_tag  = soup.find_all('h1', class_="productcard-basics__title")
        if h1_tag:
            template['title'] = h1_tag[0].get_text()

        # genre
        details = soup.find_all("a", class_="details__link ng-scope")
        template['genre'] = []
        if details:
            for a_tag in details[:-2]:
                template['genre'].append(a_tag.get_text())

        # Req_min
        req_tag = soup.find_all("div", class_="content-summary-section content-summary-offset")
        if req_tag:
            req_tag = req_tag[-1]
            template['Req_min'] = req_tag.get_text()

        # description
        h4_tags = soup.find_all("h4")
        if h4_tags:
            tag = h4_tags[0]
            description = tag.get_text() + "\n"

            for sib in tag.next_siblings:
                description = description + "\n" + sib.get_text()

            template['description'] = description

        # return
        return template












#
