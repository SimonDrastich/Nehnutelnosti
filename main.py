import re
import json
import requests

from bs4 import BeautifulSoup

webs = {
    "nehnutelnosti": {
        "domain": "https://www.nehnutelnosti.sk",
        "query": "/pezinok/predaj/?p[param1][from]=&p[param1][to]=190000&p[categories][ids]=10001.10002.10003&p[page]=%s",
        "scraped_class": "advertisement-item--content__title d-block text-truncate",
        "failure_message": "Nenašli sa žiadne výsledky"
    },
}


def scrape_webs():
    for web in webs.values():
        page = 1

        while True:
            url = web["domain"] + web["query"] % str(page)
            response = requests.post(url)
            html = response.text
            if query_failed(html, web["failure_message"]):
                break

            scrape_apartments(html, web["scraped_class"])
            page += 1


def scrape_apartments(html, scraped_class):
    soup = BeautifulSoup(html, 'html.parser')
    apartments = soup.find_all(class_=scraped_class, href=True)

    for apartment in apartments:
        if not apartment_exists(apartment.text):
            add_apartment(apartment.text)
            add_link(apartment["href"])


def query_failed(html, failure_message):
    return re.search(failure_message, html)


def add_apartment(apartment):
    with open('apartments.json', "r+") as json_file:
        data = json.loads(json_file.read())
        data['apartments'].append(apartment)
        json_file.seek(0)
        json_file.truncate()
        json.dump(data, json_file)


def apartment_exists(apartment):
    with open('apartments.json', "r") as json_file:
        data = json.loads(json_file.read())
        if apartment in data["apartments"]:
            return True
        return False


def add_link(link):
    with open('links.txt', "a") as links:
        links.write(link + "\n")


if __name__ == "__main__":
    scrape_webs()
