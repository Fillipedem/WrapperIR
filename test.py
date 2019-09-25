from bs4 import BeautifulSoup
from wrappers import SteamWrapper, NuuvemWrapper, GamesDealWrapper

page = "./pages/gamesdeal1.html"

with open(page, "r") as f:

    file_page = f.read()

wrapper = GamesDealWrapper()
extract = wrapper.extract(file_page)

for t in extract:
    print(t, " :")
    print(extract[t])
