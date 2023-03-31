from core.database.Database import Database
from model.Dish import Dish
from model.Ingredient import Ingredient


class DishRepository:

    def get_dishes(self) -> list[Dish]:
        query = """SELECT d.*, i.*, di.count FROM dishes d 
                    INNER JOIN dish_ingredients di ON d.id=di.dish_id 
                    INNER JOIN ingredients i ON i.id=di.ingredient_id"""

        dishes = []

        with Database() as con:
            cursor = con.cursor()
            cursor.execute(query)

            data = {}
            for row in cursor.fetchall():
                if row[0] not in data.keys():
                    data[row[0]] = [row]
                else:
                    data[row[0]].append(row)

            for d in data.values():
                dishes.append(self.__extract_dish(d))

        return dishes

    def create(self, dish: Dish):
        query1 = """INSERT INTO dishes VALUES(null,%s)"""
        query2 = """INSERT INTO dish_ingredients VALUES(null,%s,%s,%s)"""

        ingredients = []
        with Database() as con:
            con.autocommit = False
            cursor = con.cursor()
            cursor.execute(query1, (dish.name,))
            idx = cursor.lastrowid
            for ing in dish.ingredients:
                ingredients.append((idx, ing.idx, ing.count))
            cursor.executemany(query2, ingredients)

            con.commit()

        return idx

    def update(self, dish: Dish):
        query1 = """UPDATE dishes SET name=%s WHERE id=%s"""
        query2 = """DELETE FROM dish_ingredients WHERE dish_id=%s"""
        query3 = """INSERT INTO dish_ingredients VALUES(null,%s,%s,%s)"""

        ingredients = []
        with Database() as con:
            con.autocommit = False
            cursor = con.cursor()
            cursor.execute(query1, (dish.name, dish.idx))
            print(dish.idx)
            cursor.execute(query2, (dish.idx,))

            for ing in dish.ingredients:
                ingredients.append((dish.idx, ing.idx, ing.count))
            cursor.executemany(query3, ingredients)

            con.commit()

    def delete(self, dish: Dish):
        query1 = """DELETE FROM dishes WHERE id=%s"""

        with Database() as con:
            cursor = con.cursor()
            cursor.execute(query1, (dish.idx,))
            con.commit()

    def __extract_dish(self, data: list) -> Dish:
        """
        Convert result data to Dish object
        :param data:
        :return:
        """
        ingredients = []
        for i in data:
            ingredient = Ingredient(i[3], i[4], i[5], i[2])
            ingredients.append((ingredient, i[6]))

        dish = Dish(data[0][1], ingredients, data[0][0])

        return dish
