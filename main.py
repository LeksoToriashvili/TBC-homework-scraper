from scraper import scrape

DATABASE = "mongodb://localhost:27017/"


def main():
    scrape(DATABASE)


if __name__ == '__main__':
    main()
