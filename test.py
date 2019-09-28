from bs4 import BeautifulSoup
from wrappers import SteamWrapper, NuuvemWrapper, GamesDealWrapper, HumbleBundleWrapper, UbisoftWrapper, GOGWrapper

page = "./pages/steam2.html"

with open(page, "r") as f:

    file_page = f.read()


soup = BeautifulSoup(file_page, "html.parser")


wrapper = SteamWrapper()
extract = wrapper.extract(file_page)

for t in extract:
    print(t, " :")
    print(extract[t])
