from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

URL = "https://kulinaria.ge/receptebi/cat/konservi-da-sousebi/"
BASE_URL = "https://kulinaria.ge"


def write_to_database(database, documents):
    client = MongoClient(database)
    db = client["scrape"]

    if "scraped_data" in db.list_collection_names():
        db["scraped_data"].drop()

    collection = db["scraped_data"]

    collection.insert_many(documents)
    client.close()


def fetch_recipies(links):
    result = []

    for link in links:
        document = {}
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")

        document['title'] = soup.find("div", class_="post__title").find("h1").text
        document['url'] = link
        document['category_title'] = soup.find("div", class_="pagination-container").find_all("a")[2].text
        document['category_url'] = BASE_URL + soup.find("div", class_="pagination-container").find_all("a")[2]["href"]
        document['subcategory_title'] = soup.find("div", class_="pagination-container").find_all("a")[3].text
        document['subcategory_url'] = BASE_URL + soup.find("div", class_="pagination-container").find_all("a")[3]["href"]
        document['img_url'] = BASE_URL + soup.find("div", class_="post__img").find("img")["src"]
        document['description'] = soup.find("div", class_="post__description").text.strip()
        document['author'] = soup.find("div", class_="post__author").find("a").text.strip()

        serving = soup.find_all("div", class_="lineDesc__item")[1].text.strip()
        try:
            document['serving'] = int(serving.split(" ")[0])
        except:
            document['serving'] = 0

        ingredients = []
        for item in soup.find_all("div", class_="list__item"):
            ingredients.append(' '.join(item.text.strip().replace("&nbsp;", " ").replace("\n", " ").split()))

        steps = []
        for step in soup.find_all("div", class_="lineList__item"):
            steps.append(step.find("p").text.strip().replace("\r\n", " "))

        document['ingredients'] = ingredients
        document['steps'] = steps

        result.append(document)

    return result


def fetch_links(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', class_='box__img')
    links = []
    for div in divs:
        links.append(BASE_URL + div.find('a', href=True)['href'])

    return links


def scrape(database):
    links = fetch_links(URL)
    documents = fetch_recipies(links)
    write_to_database(database, documents)
