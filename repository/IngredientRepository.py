import pymongo

from core.database.Database import Database
from model.Ingredient import Ingredient


class IngredientRepository:

    def get_ingredients(self):
        """
        Зберігає список інгредієнтів з бази даних
        :return:
        """
        ingredients = []
        with Database("MONGO") as db:
            result = db.ingredients.find().sort("name", pymongo.ASCENDING)
            for i in result:
                ingredients.append(self.__extract_ingredient(i))

        return ingredients

    def __extract_ingredient(self, data: dict) -> Ingredient:
        """
        Конвертує дані в об'єкт Ingredient
        :param data:
        :return:
        """
        ingredient = Ingredient(data["name"], data["price"], data["count"], data["_id"])

        return ingredient
