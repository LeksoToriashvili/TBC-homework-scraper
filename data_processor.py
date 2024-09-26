from pymongo import MongoClient
from pymongo.errors import PyMongoError


class DataProcessor:
    """
    A class to process recipe data stored in a MongoDB collection.

    Attributes:
        client (MongoClient): MongoDB client object.
        db (Database): The database object.
        collection (Collection): The collection object containing recipe data.
    """

    def __init__(self, uri, database_name, collection_name):
        """
        Initializes the DataProcessor with the MongoDB connection details.

        :param uri: The MongoDB connection URI.
        :param database_name: The name of the database to use.
        :param collection_name: The name of the collection to use.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def update_recipe_counts(self):
        """ Updates the ingredient and cooking step counts for each recipe in the collection. """
        try:
            documents = self.collection.find({})
            for document in documents:
                ingredients_count = len(document['ingredients'])
                steps_count = len(document['steps'])

                self.collection.update_one(
                    {'_id': document['_id']},
                    {'$set': {
                        'ingredients_count': ingredients_count,
                        'steps_count': steps_count
                    }}
                )
        except PyMongoError as error:
            print(f'Error updating recipe counts: {error}')

    def calculate_average_recipe_metrics(self):
        """ Calculates and prints the average number of ingredients and cooking steps across all recipes. """
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': None,
                        'avg_ingredients': { '$avg': '$ingredients_count' },
                        'avg_steps': { '$avg': '$steps_count' }
                    }
                }
            ]

            total_number_of_recipes = self.collection.count_documents({})
            result = list(self.collection.aggregate(pipeline))

            if result:
                average_numbers = result[0]
                print(f"Analysis based on {total_number_of_recipes} recipes:")
                print(f"\t - Average number of ingredients per recipe: {average_numbers['avg_ingredients']:.2f}")
                print(f"\t - Average number of cooking steps per recipe: {average_numbers['avg_steps']:.2f}")
            else:
                print("No data found in the collection.")
        except PyMongoError as error:
            print(f'Error calculating averages: {error}')

    def get_largest_serving_recipe(self):
        """ Retrieves and prints the recipe with the highest number of servings. """
        try:
            pipeline = [
                { '$sort': { 'serving': -1 } },
                { '$limit': 1 }
            ]

            result = list(self.collection.aggregate(pipeline))

            if result:
                top_recipe = result[0]
                print(f"\nRecipe with the biggest number of servings: {top_recipe['title']} ({top_recipe['url']})")
                print(f"Number of servings: {top_recipe['serving']}")
            else:
                print("No recipes found.")
        except PyMongoError as error:
            print(f'Error retrieving the recipe with the largest number of servings: {error}')

    def get_author_with_most_recipes(self):
        """ Finds and prints the author who has published the most recipes. """
        try:
            pipeline = [
                { '$group': { '_id': '$author', 'recipe_count': { '$sum': 1 }, 'recipes': { '$push': '$title' } } },
                { '$sort': { 'recipe_count': -1 } },
                { '$limit': 1 }
            ]

            result = list(self.collection.aggregate(pipeline))

            if result:
                top_author = result[0]
                print(f"\nAuthor who has published the largest number of recipes: {top_author['_id']}")
                print(f"Number of recipes: {top_author['recipe_count']}")
                print('Recipes published:')
                for recipe in top_author['recipes']:
                    print(f'\t - {recipe}')
            else:
                print("No authors found.")
        except PyMongoError as error:
            print(f'Error retrieving the author with the largest number of recipes: {error}')
