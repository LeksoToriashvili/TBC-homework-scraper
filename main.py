from scraper import scrape
# from data_processor import DataProcessor

DATABASE = "mongodb://localhost:27017/"


def main():
    scrape(DATABASE)
    # uri = 'mongodb://localhost:27017/'
    # database_name = 'scrape'
    # collection_name = 'scraped_data'
    # data_processor = DataProcessor(uri, database_name, collection_name)

    # data_processor.update_recipe_counts()
    # data_processor.calculate_average_recipe_metrics()
    # data_processor.get_largest_serving_recipe()
    # data_processor.get_author_with_most_recipes()


if __name__ == '__main__':
    main()
