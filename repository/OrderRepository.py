from core.database.Database import Database
from model.Dish import Dish
from model.Order import Order


class OrderRepository:

    def get_orders(self) -> list[Order]:
        """
        Повертає список замовлень з бази даних
        :return:
        """
        orders = []
        with Database("MONGO") as db:
            result = db.orders.aggregate(
                [{"$lookup": {"from": "dishes", "localField": "dishes", "foreignField": "_id",
                              "as": "dishes"}}])
            for row in result:
                orders.append(self.__extract_order(row))

        return orders

    def create(self, order: Order, storage: list):
        """
        Зберігає замовлення у базі даних
        :param order:
        :param storage:
        :return:
        """
        with Database("MONGO") as db:
            dishIds = []
            for dish in order.dishes:
                dishIds.append(dish.idx)
            idx = db.orders.insert_one({"name": order.name, "sum": order.sum, "dishes": dishIds}).inserted_id
            for c, i in storage:
                db.ingredients.update_one({"_id": i}, {"$set": {"count": c}})

        return idx

    def __extract_order(self, data: dict) -> Order:
        """
        Конвертує дані в об'єкт Order
        :param data:
        :return:
        """
        dishes = []
        for d in data["dishes"]:
            dish = Dish(d["name"], [], d["_id"])
            dishes.append(dish)

        order = Order(data["name"], data["sum"], dishes, data["_id"])

        return order
