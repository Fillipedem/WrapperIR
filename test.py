from bs4 import BeautifulSoup
from wrappers import SteamWrapper, NuuvemWrapper, GamesDealWrapper, \
                    HumbleBundleWrapper, UbisoftWrapper, GOGWrapper, \
                    GenericWrapper
import os   # read html files names
import json # Save file as json


# read all pages from ./pages
html_pages = os.listdir("./pages/")
pages = [page.split(".")[0] for page in html_pages]

# Wrapper
wrapper = GenericWrapper()

for page in pages:

    # open
    with open("./pages/" + page + ".html", "r") as file:
        html = file.read()
        info = wrapper.extract(html)

    # save
    with open("./info_pages/" + page + ".json", 'w') as file:
        file.write(str(info))
