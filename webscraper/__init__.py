import cfscrape
from bs4 import BeautifulSoup


def webscraper_mega_sena_number():

    URL = "https://www.google.com/search?q=caixa+mega+sena"

    scraper = cfscrape.create_scraper()
    html = scraper.get(URL).content
    soup = BeautifulSoup(html, "lxml")

    span_list = [x.extract() for x in soup.find_all('span')]
    winner_numbers = []

    for span in span_list:
        if span.text is not None and span.text.isnumeric():
            winner_numbers.append(int(span.text))

    return winner_numbers
