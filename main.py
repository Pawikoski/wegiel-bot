from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()

url = 'https://sklep.pgg.pl/'
response = session.get(url)
response.html.render()

soup = BeautifulSoup(response.html.html, 'html.parser')

products = soup.findAll("div", {"itemtype": "http://schema.org/Product"})

for product in products:
    product_name_raw = product.find("h1")
    product_name = product_name_raw.text.strip() if product_name_raw else None

    product_url_raw = product_name_raw.find("a")
    product_url = product_url_raw['href'] if product_url_raw else None

    product_price_raw = product.find("meta", {"itemprop": "price"})
    product_price = float(product_price_raw['content'].replace(",", ".")) if product_price_raw else None

    print(product_name, product_price, product_url)

session.close()
