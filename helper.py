"""
Funções de ajuda para a extração
"""
from bs4 import NavigableString

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


def get_div_table_dict():
    pass

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
