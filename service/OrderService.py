from model.Dish import Dish
from model.IngredientStorage import IngredientStorage
from model.Order import Order
from repository.DishRepository import DishRepository
from repository.OrderRepository import OrderRepository


class OrderService:
    MARKUP = 105

    def __init__(self):
        self.ist = IngredientStorage()

    def order(self, dishes: list[Dish]) -> Order:
        """
        Створення замовлення
        :param dishes:
        :return:
        """
        name = self.__get_name(dishes)
        overflow = self.check_ingredients(dishes)
        if len(overflow) != 0:
            raise ValueError("Недостатньо інградієнтів \"{}\"".format('\" \"'.join([i.name for i in overflow])))
        sum = self.get_dishes_sum(dishes)
        order = Order(name, sum, dishes)
        OrderRepository().create(order, self.ist.to_update())

        return order

    def get_dishes(self):
        """
        Повертає усі страви з обрахованою ціною
        :return:
        """
        dishes = DishRepository().get_dishes()
        for dish in dishes:
            dish.price = self.get_dish_price(dish)

        return dishes

    def __get_name(self, dishes) -> str:
        """
        Генерує назву замовлення
        :param dishes:
        :return:
        """
        names = [dish.name for dish in dishes]
        return ", ".join(names)

    def check_ingredients(self, dishes: list) -> list[Dish]:
        """
        Перевірка доступності страв для замовлення
        Перевірка, чи достатньо інгредієнтів на складі
        :param dishes:
        :return:
        """
        storage = {}
        for dish in dishes:
            for ing, count in dish.ingredients:
                if ing.idx in storage:
                    storage[ing.idx] += count * dish.count
                else:
                    storage[ing.idx] = count * dish.count

        overflow = []

        for idx, amount in storage.items():
            if self.ist.storage[idx].count < amount:
                overflow.append(self.ist.storage[idx])
            self.ist.storage[idx].count -= amount

        return overflow

    def get_dishes_sum(self, dishes: list) -> float:
        """
        Обраховує ціну замовлення
        :param dishes:
        :return:
        """
        amount = 0
        for dish in dishes:
            amount += self.get_dish_price(dish) * dish.count
        return amount

    def get_dish_price(self, dish: Dish) -> float:
        """
        Обраховує ціну страви
        :param dish:
        :return:
        """
        price = 0
        for ing, count in dish.ingredients:
            price += round((ing.price * count / 1000) * (100 + self.MARKUP) / 100)

        return price
