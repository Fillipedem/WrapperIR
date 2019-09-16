"""
Funções de ajuda para a extração
"""

def get_div_text(tag_div):
    """
    Retornar o texto de uma tag div
    input: BeautifulSoup tag
    output: str
    """
    for br in tag_div.find_all("br"):
        br.replace_with("\n")

    return tag_div.get_text()
