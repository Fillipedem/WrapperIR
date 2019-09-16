from bs4 import BeautifulSoup
from wrappers import SteamWrapper

page = "./pages/steam2.html"
with open(page, "r") as f:
    file_steam = f.read()

# parser
steam_wrapper = SteamWrapper()
saida = steam_wrapper.extract(file_steam)

for i in saida:
    print(saida[i])
