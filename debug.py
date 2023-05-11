import json

from repository.DishRepository import DishRepository
from repository.IngredientRepository import IngredientRepository
from repository.OrderRepository import OrderRepository

ir = IngredientRepository()
dr = DishRepository()
orr = OrderRepository()


def encoder(obj):
    return obj.to_dict()


# Виведення даних з бази в консоль у форматі JSON

print("INGREDIENTS")
print(json.dumps(ir.get_ingredients(), default=encoder))
print("DISHES")
print(json.dumps(dr.get_dishes(), default=encoder))
print("ORDERS")
print(json.dumps(orr.get_orders(), default=encoder))
