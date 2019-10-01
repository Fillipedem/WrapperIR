from selenium import webdriver

# var
url = "https://www.wingamestore.com/product/10691/GreedFall/"
file = "./pages/winstore2.html"

# OpenBrowser
browser = webdriver.Chrome()
browser.get(url)

# Download HTML
innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string

with open(file, 'w') as f:
    f.write(innerHTML)
