# GET. POST, PUT, PATCH, DELETE
from pprint import pprint

import requests
from bs4 import BeautifulSoup


URL = "https://rezka.ag/series/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_data(html, size=None):
    soup = BeautifulSoup(html, 'html.parser')
    size = int(size) if size else None
    items = soup.find_all("div", class_="b-content__inline_item", limit=size)
    series = []
    for item in items:
        info = item.find('div', class_="b-content__inline_item-link").find('div').string.split(', ')
        card = {
            "title": item.find('div', class_="b-content__inline_item-link").find('a').string,
            "url": item.find('div', class_="b-content__inline_item-link").find('a').get("href"),
            "status": item.find("span", class_="info").getText(),
            "year": info[0],
            "country": info[1],
            "genre": info[2],
            "image": item.find("img").get("src")
        }
        series.append(card)

    return series


def parser(size=None):
    html = get_html(URL)
    if html.status_code == 200:
        series = get_data(html.text, size)
        return series
    raise Exception("Error in parser!")

