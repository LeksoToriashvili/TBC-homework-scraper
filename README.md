# Recipe Scraper and Data Analyzer

This project collects recipe data from the 'Canning & Sauces' category of a Georgian cooking website [kulinaria.ge](https://kulinaria.ge),
stores it in a MongoDB database, and performs various analyses on the collected data, such as the average number of ingredients, 
cooking steps, the recipe with the largest servings, and the author with the most published recipes.

## Features
### Web Scraper

- Scrapes recipe data from the "Canning & Sauces" category of [kulinaria.ge](https://kulinaria.ge).
- Uses Python’s `ThreadPoolExecutor` to fetch recipe data concurrently.
- Collects information such as recipe title, URL, main category, subcategory, image URL, description, author, serving size, ingredients, and cooking steps.
- Stores the collected data in a MongoDB database.

### Data Processor

- Updates ingredient and cooking step counts for each recipe.
- Calculates average number of ingredients and cooking steps across all recipes.
- Retrieves the recipe with the highest number of servings.
- Finds the author who has published the largest number of recipes.

## Project Structure

- `scraper.py` - Contains the `Scraper` class that handles scraping the website and storing the data in MongoDB.
- `data_processor.py` - Contains the `DataProcessor` class for analyzing the scraped data.
- `main.py` - The main script that ties everything together and runs the scraping and analysis processes.
- `requirements.txt` - Contains a list of packages or libraries needed to work on the project.
- `README.md` - Project description.

## Requirements

- Python 3.7+
- MongoDB
- Python libraries (listed in requirements.txt):
  - `requests`
  - `beautifulsoup4`
  - `pymongo`
  - `concurrent.futures`
  - `bs4`

## Setup and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/LeksoToriashvili/TBC-homework-scraper.git
   cd main.py

2. Install the required packages:
    ```bash
    pip install -r requirements.txt

3. Make sure MongoDB is running locally or adjust the connection URI to point to your MongoDB instance.
4. Run the `main.py`.
    ```bash
   python main.py

## Configuration
The main configuration parameters are set in the `main.py` file:

- `uri`: MongoDB connection URI (default: "mongodb://localhost:27017/").
- `database_name`: Name of the MongoDB database (default: 'scrape')
- `collection_name`: Name of the MongoDB collection (default: 'scraped_data')

You can modify these parameters as needed to match your MongoDB setup.

## Note

This scraper is designed for educational purposes. Please be respectful of the website's resources and terms of service when using this tool.
   
