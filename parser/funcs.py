import requests

from bs4 import BeautifulSoup


def parse_institutes():
    url = "https://www.findaphd.com/phds/self-funded/?01M0"
    html = requests.get(url).text

    soup = BeautifulSoup(html, "lxml")
    countries_option = soup.find("select", id="InstInput").find_all("option")
    countries = [country.string.split('(')[0].strip() for country in countries_option]
    return countries[1:]


def tag_is_discipline(tag):
    if tag.has_attr("href"):
        result = any((tag.name == "span", tag.attrs["href"].split("/")[-1].startswith("?20")))
        return result
    else:
        return tag.name == "span"


def tag_is_funded(tag):
    if tag.name == "a":
        if "fa-wallet" in tag.span.i.attrs["class"]:
            return True
    return False


def parse_detail_if_not_parsed(func):
    def wrapper(self):
        try:
            func(self)
        except AttributeError:
            print("=============================================================================================================================================================")
            html = requests.get(self.DOMAIN + self.url).text
            self.detail_soup = BeautifulSoup(html, "lxml")
            func(self)
    return wrapper


def parse_countries():
    url = "https://www.findaphd.com/phds/self-funded/?01M0"
    html = requests.get(url).text

    soup = BeautifulSoup(html, "lxml")
    countries_option = soup.find("select", id="CountryInput").find_all("option")
    countries = [country.string.split('(')[0].strip() for country in countries_option]
    return countries[1:]


def get_keyboard_button(buttons):
    result = []
    row = []
    for i, button in enumerate(buttons):
        if i % 2 == 1:
            result.append(row)
            row = [button, ]
        else:
            row.append(button)
    result.append(row)
    return result