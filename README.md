# Recipe Scraper and Analyzer

This project collects recipe data from the 'Canning & Sauces' category of a Georgian cooking website [kulinaria.ge](https://kulinaria.ge),
stores it in a MongoDB database, and performs various analyzes on the collected data. The project is divided 
into two main components:

- **Web Scraper**: Collects recipe data from the website.
- **Data Processor**: Analyzes the collected data and provides insights.

## Requirements

- Python 3.7+
- MongoDB

## Setup and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/LeksoToriashvili/TBC-homework-scraper.git
   cd main.py

2. Install the required packages:
    ```bash
    pip install -r requirements.txt

3. Set up a MongoDB database and note down the connection URI.
4. Create a .env file in the project root and add your MongoDB URI:
    ```bash
    MONGODB_URI="mongodb://localhost:27017/"

5. Run the `main.py`.
    ```bash
   python main.py

## Project Structure

- `scraper.py` - Web scraping script.
- `data_processor.py` - Data analysis class.
- `main.py` - Main script to run the data processor.
- `requirements.txt` - Project dependencies.
- `README.md` - Project documentation.

## Features
### Web Scraper

- Scrapes recipe data from the "Canning & Sauces" category of [kulinaria.ge](https://kulinaria.ge).
- Collects information such as recipe title, URL, main category, subcategory, image URL, description, author, serving size, ingredients, and cooking steps.
- Stores the collected data in a MongoDB database.

### Data Processor

- Updates ingredient and cooking step counts for each recipe.
- Calculates average number of ingredients and cooking steps across all recipes.
- Retrieves the recipe with the highest number of servings.
- Finds the author who has published the largest number of recipes.


   
