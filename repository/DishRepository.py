from bson import ObjectId

from core.database.Database import Database
from model.Dish import Dish
from model.Ingredient import Ingredient


class DishRepository:

    def get_dishes(self) -> list[Dish]:
        """
        Повертає список страв з бази даних
        :return:
        """
        dishes = []

        with Database("MONGO") as db:
            result = db.dishes.aggregate(
                [{"$lookup": {"from": "ingredients", "localField": "ingredients", "foreignField": "_id",
                              "as": "ingredients"}}])
            for row in result:
                dishes.append(self.__extract_dish(row))

        return dishes

    def create(self, dish: Dish):
        """
        Зберігає страву в базі даних
        :param dish:
        :return:
        """
        with Database("MONGO") as db:
            ingredientIds = []
            for ing in dish.ingredients:
                ingredientIds.append(ing.idx)
            idx = db.dishes.insert_one({"name": dish.name, "ingredients": ingredientIds}).inserted_id

        return idx

    def update(self, dish: Dish):
        """
        Оновлює страву в базі даних
        :param dish:
        :return:
        """
        with Database("MONGO") as db:
            ingredientIds = []
            for ing in dish.ingredients:
                ingredientIds.append(ing.idx)
            db.dishes.update_one({"_id": dish.idx}, {"$set": {"name": dish.name, "ingredients": ingredientIds}})

    def delete(self, dish: Dish):
        """
        Видаляє страву з бази даних
        :param dish:
        :return:
        """
        with Database("MONGO") as db:
            db.dishes.delete_one({"_id": ObjectId(dish.idx)})

    def __extract_dish(self, data: dict) -> Dish:
        """
        Конвертує дані в об'єкт Dish
        :param data:
        :return:
        """
        ingredients = []
        for i in data["ingredients"]:
            ingredient = Ingredient(i["name"], i["price"], i["count"], i["_id"])
            ingredients.append((ingredient, 200))

        dish = Dish(data["name"], ingredients, data["_id"])

        return dish
