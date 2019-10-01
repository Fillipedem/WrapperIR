"""
Funções de ajuda para a extração
"""
from bs4 import NavigableString
import re

def get_div_text(tag_div):
    """
    Retornar o texto de uma tabela
    input: BeautifulSoup tag
    output: str
    """
    for br in tag_div.find_all("br"):
        br.replace_with("\n")

    return tag_div.get_text()


def get_div_dict(tag_div):
    template = {}
    tmp_tag = None

    for tag in tag_div:

        # Checando se é um valor
        if isinstance(tag, NavigableString) and len(tag) > 4:
            template[tmp_tag].append(tag)
            continue

        if tag.name == "a":
            template[tmp_tag].append(tag.text)

        # Checando se o valor é um Atributo
        if tag.name == "b":
            tmp_tag = tag.text
            template[tmp_tag] = []
    #endfor

    return template


def get_meta_dict(meta_tags):
    """
    Retorna uma lista com os itemprop + content de cada tag meta
    """
    meta_dict = {}

    for meta in meta_tags:
        property = meta.get("itemprop")
        content = meta.get("content")

        if property not in meta_dict:
            meta_dict[property] = []

        meta_dict[property].append(content)

    return meta_dict


def get_children_tags(tag, children_tag):
    """
    Retorna a lista com as strings de todas as tags iguais a children_tag
    """
    ans = []

    tags = tag.find_all(children_tag)
    for tag in tags:
        ans.append(tag.get_text())

    return ans


def get_navigable_strings(tag):
    """
    Returns all NavigableStrings from the tag children_tag

    input: bs Tag
    output: str list
    """
    ans = []
    children = list(tag.children)

    for c in children:
        if isinstance(c, NavigableString) and c != "\n":
            ans.append(c.strip())

    return ans


def get_from_list(idx, all_tags, tag_text):
    ans = []
    split = lambda x: re.split('\n|,|-', x)

    tmp = all_tags[idx].next_sibling
    if isinstance(tmp, NavigableString) and len(tmp) >= 2:
        return [tmp.strip()]

    tmp = all_tags[idx + 1]
    if tmp.name == "div":
        ans = get_div_text(tmp)
    else:
        ans = tmp.get_text()

    # ajeitando nomes
    ans = split(ans)
    ans = [x for x in ans if len(x) > 1]
    ans = [word.strip() for word in ans]

    return ans
