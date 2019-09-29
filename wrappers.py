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
from helper import get_div_text, get_div_dict, get_meta_dict, \
                    get_children_tags, get_navigable_strings
from wrapper import Wrapper, game_template
from py_common_subseq import find_common_subsequences
import json


class GenericWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template.copy()

        # find title
        h1_tags = soup.find_all("h1")

        if h1_tags:
            title = h1_tags[0].get_text().strip()

            template['title'] = title.split("Buy ")[-1]


        # !!game details!!
        """
        div_tags = soup.find_all("div")
        for tag in div_tags:
            if "details" in tag.get_text().lower() :
                for tag_a in tag.find_all("a"):
                    print(tag_a.get_text())
        """

        # Requirements
        #desc = soup.find_all("div", "description")


        # About the game
        h2_tags = soup.find_all("h2")

        for tag in h2_tags:


            tag_text = tag.get_text().lower()

            if "about" in tag_text or "description" in tag_text:
                parent = tag.parent

                template["description"] = parent.get_text().split("System Requirements")[0]

        return template


class SteamWrapper(Wrapper):

    def __init__(self):
        pass

    def extract(self, html_page):
        soup = BeautifulSoup(html_page, "html.parser")

        template = game_template

        # Title/Genre Dev/Pub
        # O primeiro block div com nome "details_block"
        # contem os atributos: Title/Genre Dev/Pub
        div_tags = soup.find_all("div")
        for tag in div_tags:
            if tag.get("class") == ["details_block"]:

                # Title/Genre
                tmp_tag = get_div_dict(tag)
                if tmp_tag:
                    template['title'] = tmp_tag['Title:'][0]
                    template['genre'] = tmp_tag['Genre:']

                # pub and dev
                tmp_tag = tag.findAll("div")
                if tmp_tag:
                    template['dev'] = get_div_dict(tmp_tag[0])
                    template['pub'] = get_div_dict(tmp_tag[1])

                # break
                break # Em alguns sites existem oturos blocks "details_blocks" que deve ser ignorado

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

        # dev/pub
        for tag in soup.find_all("strong"):
            if tag.get_text() == "Developer:":
                template['dev'] = tag.next_sibling

            if tag.get_text() == "Publisher:":
                template['pub'] = tag.next_sibling

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

        template['genre'] = genres_list

        # dev
        dev_tags = soup.find_all("div", class_="property-view developers-view js-admin-edit")
        if dev_tags:

            template['dev'] = get_children_tags(dev_tags[0], 'a')

        # pub
        pub_tags = soup.find_all("div", class_="property-view publishers-view js-admin-edit")
        if pub_tags:

            template['pub'] = get_children_tags(pub_tags[0], 'a')

        # requirements
        reqs_div = soup.find_all("div", class_="property-view system_requirements-view expandable js-admin-edit collapsed")
        if reqs_div:
            reqs = list(reqs_div[0])[0]
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

        # genre/dev/pub
        span_tags = soup.find_all("span", class_="product-details-info-name")
        if span_tags and len(span_tags) >= 6:
            genre = span_tags[3].parent
            dev = span_tags[5].parent
            pub = span_tags[4].parent

            template['genre'] = get_navigable_strings(genre)
            template['pub'] = get_navigable_strings(pub)
            template['dev'] = get_navigable_strings(dev)

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

        # dev/pub/genre
        details = soup.find_all("a", class_="details__link ng-scope")

        if details:

            for a_tag in details:
                if "Publisher" in a_tag.get("gog-track-event"):
                    template['pub'].append(a_tag.get_text())
                elif "Developer" in a_tag.get("gog-track-event"):
                    template['dev'].append(a_tag.get_text())
                else:
                    template['genre'].append(a_tag.get_text())

        # Req_min
        req_tag = soup.find_all("div", class_="system-requirements")
        if req_tag:
            template['Req_min'] = req_tag[0].get_text()

        # description
        description = soup.find_all("div", class_="description")
        if description:
            template['description'] = description[0].get_text()

        # return
        return template












#
