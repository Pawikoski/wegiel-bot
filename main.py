import random

from bs4 import BeautifulSoup

from datetime import datetime
import time

import requests
import re

from fake_useragent import UserAgent

ua = UserAgent()
url = 'https://sklep.pgg.pl/'

while True:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Host": "httpbin.org",
        "Sec-Ch-Ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": ua.random,
        "X-Amzn-Trace-Id": "Root=1-60ff12bb-55defac340ac48081d670f9d"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(str(response.content.decode('unicode-escape')), 'html.parser')
    products = soup.findAll("produkt-box-component")
    print(len(products))
    # print(soup)
    for product in products:
        product_string = product[':produkt']
        # print(product_string)
        name = re.findall(r'\"nazwa\":\"[A-Za-zęółśążźćń\s*]*\",\"opis\"', product_string)[0].replace(',"opis"', "").strip()
        is_available = re.findall(r'\"czy_dostepny\":[A-Za-z]*', product_string)[0]
        if "false" in is_available:
            is_available = False
        else:
            is_available = True

        if is_available:
            with open(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 'w') as f:
                f.write(name)

    time.sleep(random.randint(200, 400))
