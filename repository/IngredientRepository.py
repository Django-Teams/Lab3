from core.database.Database import Database
from model.Ingredient import Ingredient


class IngredientRepository:

    def get_ingredients(self):
        query = """SELECT * FROM ingredients ORDER BY name"""

        ingredients = []

        with Database() as con:
            cursor = con.cursor()
            cursor.execute(query)

            for i in cursor.fetchall():
                ingredients.append(self.__extract_ingredient(i))

        return ingredients

    def __extract_ingredient(self, data: list) -> Ingredient:
        """
        Convert result data to Ingredient object
        :param data:
        :return:
        """
        ingredient = Ingredient(data[1], data[2], data[3], data[0])

        return ingredient
