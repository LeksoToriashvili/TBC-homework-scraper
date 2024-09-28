import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os


class Scraper:
    def __init__(self, uri, database, collection):
        self.uri = uri
        self.database = database
        self.collection = collection
        self._URL = "https://kulinaria.ge/receptebi/cat/konservi-da-sousebi/?page="
        self._BASE_URL = "https://kulinaria.ge"
        self.max_number_of_requests = 100
        self._recipes = []
        self._status = ""

    def scrape(self):
        try:
            links = self.__fetch_links()
            self.__fetch_recipes(links)
            self.__store_data()
            self._status = "success"
        except Exception as e:
            self._status = e

    def __fetch_links(self):
        i = 0
        links = set()

        while True:
            i += 1
            if i > self.max_number_of_requests:
                break

            response = requests.get(self._URL + str(i))

            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_='box__img')
            new_links = set()
            for div in divs:
                new_links.add(self._BASE_URL + div.find('a', href=True)['href'])

            if links == links | new_links:
                break

            links = links.union(new_links)

        return list(links)

    def __fetch_recipes(self, links):
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            for link in links:
                executor.submit(self.__fetch_recipe, link)

    def __store_data(self):
        client = MongoClient(self.uri)
        db = client[self.database]

        if self.collection in db.list_collection_names():
            db[self.collection].drop()

        collection = db[self.collection]

        collection.insert_many(self._recipes)
        client.close()

    def __fetch_recipe(self, link):
        document = {}
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")

        document['title'] = soup.find("div", class_="post__title").find("h1").text
        document['url'] = link
        document['category_title'] = soup.find("div", class_="pagination-container").find_all("a")[2].text
        document['category_url'] = self._BASE_URL + soup.find("div", class_="pagination-container").find_all("a")[2]["href"]
        document['subcategory_title'] = soup.find("div", class_="pagination-container").find_all("a")[3].text
        document['subcategory_url'] = self._BASE_URL + soup.find("div", class_="pagination-container").find_all("a")[3][
            "href"]
        document['img_url'] = self._BASE_URL + soup.find("div", class_="post__img").find("img")["src"]
        document['description'] = soup.find("div", class_="post__description").text.strip()
        document['author'] = soup.find("div", class_="post__author").find("a").text.strip()

        serving = soup.find_all("div", class_="lineDesc__item")[1].text.strip()
        try:
            document['serving'] = int(serving.split(" ")[0])
        except:
            document['serving'] = "N/A"

        ingredients = []
        for item in soup.find_all("div", class_="list__item"):
            ingredients.append(' '.join(item.text.strip().replace("&nbsp;", " ").replace("\n", " ").split()))

        steps = []
        for step in soup.find_all("div", class_="lineList__item"):
            steps.append(step.find("p").text.strip().replace("\r\n", " "))

        document['ingredients'] = ingredients
        document['steps'] = steps

        self._recipes.append(document)

    @property
    def status(self):
        return self._status
