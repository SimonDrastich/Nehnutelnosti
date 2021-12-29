import re
import json
import requests

from bs4 import BeautifulSoup

query = "/pezinok/predaj/?p[param1][from]=&p[param1][to]=180000&p[categories][ids]=10001.10002.10003&p[page]="
url = "https://www.nehnutelnosti.sk" + query
failure = "Nenašli sa žiadne výsledky"


def scrape_nehnutelnosti():
    page = 1
    while True:
        response = requests.post(url + str(page))
        text = response.text
        if re.search(failure, text):
            break

        # WEB SCRAPING
        soup = BeautifulSoup(text, 'html.parser')
        block_of_flats = soup.find_all(class_="advertisement-item--content__title d-block text-truncate", href=True)
        for block in block_of_flats:
            if not block_exists(block.text):
                add_block(block.text)
                add_link(block["href"])
        page += 1


def add_block(block):
    with open('byty.json', "r+") as json_file:
        data = json.loads(json_file.read())
        data['byty'].append(block)
        json_file.seek(0)
        json_file.truncate()
        json.dump(data, json_file)


def block_exists(block):
    with open('byty.json', "r") as json_file:
        data = json.loads(json_file.read())
        if block in data["byty"]:
            return True
        return False


def add_link(link):
    with open('links.txt', "a") as links:
        links.write(link + "\n")


if __name__ == "__main__":
    scrape_nehnutelnosti()
