"""
Classe abstratar para o Wrapper
"""

class Wrapper():

    def __init__(self):
        pass

    def extract(self, html_page):
        """
        Retorna um dicionario com o conteudo do extraido da pagina

        input: html_page: arquivo html como str
        output: template_dict
        """
        pass


game_template = {"title": None, "genre": [], "pub": [], "dev": [],
                 "Req_max": None, "Req_min": None, "description": None}
