import random
import re
from decimal import Decimal
from random import randint

import requests
from bs4 import BeautifulSoup as bs

from shop.models import Product

URL_SCRAPING = 'https://www.sportmaster.ru/catalog/zhenskaya_obuv/krossovki/'
URL_SCRAPING_DOMAIN = 'https://www.sportmaster.ru'


class ScrapingError(Exception):
    pass


class ScrapingTimeoutError(ScrapingError):
    pass


class ScrapingHTTPError(ScrapingError):
    pass


class ScrapingOtherError(ScrapingError):
    pass


def scraping():
    try:
        resp = requests.get(URL_SCRAPING, timeout=10.0)
    except requests.exceptions.Timeout:
        raise ScrapingTimeoutError("request timed out")
    except Exception as e:
        raise ScrapingOtherError(f'{e}')

    if resp.status_code != 200:
        raise ScrapingHTTPError(f"HTTP {resp.status_code}: {resp.text}")

    data_list = []
    html = resp.text
    soup = bs(html, 'html.parser')
    blocks = soup.find_all('div', attrs={'data-selenium': 'product-card'})
    for block in blocks:
        data = {}

        name = block.find('a', attrs={'data-selenium': 'product-name'}).get_text().strip()
        data['name'] = name

        image_url = block.find('a', attrs={'data-selenium': 'product-card-image'})
        image_link = URL_SCRAPING_DOMAIN + image_url.get('href')
        resp_img = requests.get(image_link)
        soup = bs(resp_img.text, 'html.parser')
        img = soup.find('img', attrs={'alt': f'{name}'}).get('src')
        data['image_url'] = img

        try:
            desc_url = block.find('a', attrs={'data-selenium': 'product-card-image'})
            desc_link = URL_SCRAPING_DOMAIN + desc_url.get('href')
            desc_link = requests.get(desc_link)
            soup = bs(desc_link.text, 'html.parser')
            note = soup.find('span', class_='sm-text sm-text--text-12 sm-text--regular a_IDo').text
            data['note'] = note
        except Exception:
            continue

        price_raw = block.find('span', attrs={'data-selenium': 'amount'}).text
        price_cl = price_raw.replace('₽', '')
        price = Decimal(price_cl.replace(' ', ''))
        print(price)
        data['price'] = price

        unit = 1000
        data['unit'] = unit

        code = random.randint(11111, 99999)
        data['code'] = code

        data_list.append(data)

    print(data_list)

    for item in data_list:
        # if not Product.objects.filter(code=item['code']).exists():
        Product.objects.create(
            unit=item['unit'],
            name=item['name'],
            code=item['code'],
            price=item['price'],
            note=item['note'].strip(),
            image_url=item['image_url'],
        )
    return data_list


if __name__ == '__main__':
    scraping()
