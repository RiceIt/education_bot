import abc
import bs4
import requests

from bs4 import BeautifulSoup

from parser.funcs import tag_is_discipline, tag_is_funded, parse_detail_if_not_parsed


class AbstractPlatform(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def get_program_list(cls) -> bs4.ResultSet:
        pass

    def __init__(self, soup) -> None:
        self.soup = soup

    @abc.abstractmethod
    def parse_url(self) -> None:
        pass

    @abc.abstractmethod
    def parse_slug(self) -> None:
        pass

    @abc.abstractmethod
    def parse_title(self) -> None:
        pass

    @abc.abstractmethod
    def parse_location(self) -> None:
        pass

    @abc.abstractmethod
    def parse_institute(self) -> None:
        pass

    @abc.abstractmethod
    def parse_department(self) -> None:
        pass

    @abc.abstractmethod
    def parse_type(self) -> None:
        pass

    @abc.abstractmethod
    def parse_funding(self) -> None:
        pass

    @abc.abstractmethod
    def parse_subjects(self) -> None:
        pass

    @abc.abstractmethod
    def parse_description(self) -> None:
        pass


class FindAPhD(AbstractPlatform):
    DOMAIN = "https://www.findaphd.com"

    @classmethod
    def get_program_list(cls) -> bs4.ResultSet:
        url = "https://www.findaphd.com/phds/?Show=M"
        html = requests.get(url).text

        soup = BeautifulSoup(html, "lxml")
        programs = soup.find_all("div", class_="phd-result-row-standard")
        return programs

    def parse_url(self) -> None:
        self.url = self.soup.div.div.find_all("div")[2].h3.find_all("a")[1].attrs["href"].strip()

    def parse_slug(self) -> None:
        self.slug = self.url.split("/")[-1][2:].strip()

    def parse_title(self) -> None:
        self.title = self.soup.div.div.find_all("div")[2].h3.find_all("a")[1].text.strip()

    def parse_location(self) -> None:
        self.location = self.soup.div.div.find_all("div")[2].find_all("div")[0].a.img.attrs["title"].strip()

    def parse_institute(self) -> None:
        self.institute = self.soup.div.div.find_all("div")[2].find_all("div")[0].a.span.text.strip()

    def parse_department(self) -> None:
        self.department = self.soup.div.div.find_all("div")[2].find_all("div")[0].find_all("a")[1].text.strip()

    def parse_type(self) -> None:
        self.type = self.soup("div", class_="phd-icon-area")[0].find_all("a")[1].span.text.strip()

    def parse_funding(self) -> None:
        self.funding = self.soup.div.div.find_all("div")[2].find_all("div")[-1].find_all(tag_is_funded)[0].span.text.strip().split("(")[-1].split(")")[0]

    @parse_detail_if_not_parsed
    def parse_subjects(self) -> None:
        elements = self.detail_soup.find("div", class_="phd-data__container").find_all(tag_is_discipline)
        self.subjects = [a.text for a in elements]

    @parse_detail_if_not_parsed
    def parse_description(self) -> None:
        description = self.detail_soup.find("div", class_="phd-sections__description")
        content = description.find("div", class_="phd-sections__content")
        self.description = tuple(content.children)


class Euraxess(AbstractPlatform):
    @classmethod
    def get_program_list(cls) -> bs4.ResultSet:
        url = "https://euraxess.ec.europa.eu/funding/search"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        html = requests.get(url, headers=headers).text

        soup = BeautifulSoup(html, "lxml")
        programs = soup.find_all("div", class_="view-content")[0].find_all("div", class_="views-row")
        return programs

    def parse_url(self) -> None:
        self.url = self.soup.find_all("div", class_="row")[1].find_all("div")[0].h2.a.attrs["href"].strip()

    def parse_slug(self) -> None:
        self.slug = self.url.split("/")[-1].strip()

    def parse_title(self) -> None:
        self.title = self.soup.find_all("div", class_="row")[1].find_all("div")[0].h2.a.string.strip()

    def parse_location(self) -> None:
        self.location = self.soup.find_all("div", class_="row")[1].find_all("div")[1].ul.find_all("li")[3].div.find_all("div")[1].string.strip()

    def parse_institute(self) -> None:
        self.institute = self.soup.find_all("div", class_="row")[1].find_all("div")[1].ul.find_all("li")[2].div.find_all("div")[1].string.strip()

    def parse_department(self) -> None:
        pass

    def parse_type(self) -> None:
        pass

    def parse_funding(self) -> None:
        pass

    def parse_subjects(self) -> None:
        pass

    def parse_description(self) -> None:
        pass
