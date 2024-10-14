import requests
from bs4 import BeautifulSoup
import pandas as pd

class kinpet_parser:
    def __init__(self):
        self.st_accept = "text/html"
        self.st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
        self.card_title = 'breed-sale-card__title'
        self.card_location = 'animal-location__text'
        self.headers = {
            "Accept": self.st_accept,
            "User-Agent": self.st_useragent
        }
        self.max_page = 78

    def process_database(self, database):
        database['title'] = database['title'].apply(lambda x: str(x.text).replace("\n", ""))
        database['description'] = database['description'].apply(lambda x: str(x.text).replace("\n", ""))
        database['url'] = database['url'].apply(lambda x: 'https://kinpet.ru' + str(x))
        database['location'] = database['location'].apply(lambda x: str(x.text).replace("\n", ""))
        return database

    def get_lost_pets_database(self):
        s = requests.Session()
        s.headers.update(self.headers)
        frames = []
        for page_searching in range(1, self.max_page + 1):
            req = s.get(f"https://kinpet.ru/rossiya/poteryavshiesya/?nav=page-{page_searching}")
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            a_tags = soup.find_all('a', class_=self.card_title)
            urls = [a.get('href') for a in a_tags]
            p_tags = soup.find_all('p')[:len(a_tags)]
            location_tags = soup.find_all('a', class_=self.card_location)
            appen_database = pd.DataFrame({
                'title': a_tags,
                'description': p_tags,
                'url': urls,
                'location': location_tags
            })
            frames.append(appen_database)
        pets_database = pd.concat(frames, ignore_index=True)
        return self.process_database(pets_database)
parser = kinpet_parser()
parser.get_lost_pets_database().to_csv('found_lost_pets.csv')