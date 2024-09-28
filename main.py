from scraper import Scraper
from data_processor import DataProcessor


def main():
    uri = "mongodb://localhost:27017/"
    database_name = 'scrape'
    collection_name = 'scraped_data'

    scraper = Scraper(uri, database_name, collection_name)

    scraper.scrape()

    if scraper.status == 'success':
        data_processor = DataProcessor(uri, database_name, collection_name)
        data_processor.update_recipe_counts()
        data_processor.calculate_average_recipe_metrics()
        data_processor.get_largest_serving_recipe()
        data_processor.get_author_with_most_recipes()
    else:
        print(scraper.status)


if __name__ == '__main__':
    main()
