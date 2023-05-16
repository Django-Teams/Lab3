from pymongo import MongoClient

# Для створення бази потрібно виконати команду "use django" у консолі Mongosh

client = MongoClient()

db = client["django"]

# Додавання в базу інгредієнтів
data = [
    {"name": "Спагетті", "price": 40, "count": 11550},
    {"name": "Помідор", "price": 96, "count": 2200},
    {"name": "Куряче філе", "price": 140, "count": 4600},
    {"name": "Гриби печериці", "price": 109, "count": 1900},
    {"name": "Сир твердий", "price": 300, "count": 900},
    {"name": "Рис", "price": 60, "count": 3850},
    {"name": "Картопля", "price": 20, "count": 29750},
    {"name": "Морква", "price": 20, "count": 9900},
    {"name": "М'ясо свинини", "price": 210, "count": 2400},
    {"name": "Куряче яйце", "price": 100, "count": 6000},
    {"name": "Ізюм", "price": 150, "count": 1250},
]
# Видалення і створення таблиці ingredients
if "ingredients" in db.list_collection_names():
    db.drop_collection("ingredients")
ingredients = db.create_collection("ingredients")
insertIds = ingredients.insert_many(data).inserted_ids

# Додавання в базу страв
data = [
    {"name": "Паста з куркою та грибами", "ingredients": [insertIds[3], insertIds[2], insertIds[1], insertIds[0]]},
    {"name": "Картопля з м'ясом", "ingredients": [insertIds[6], insertIds[8], insertIds[4], insertIds[0]]},
    {"name": "Плов з овочами", "ingredients": [insertIds[10], insertIds[8], insertIds[7], insertIds[5], insertIds[1]]},
    {"name": "Рис з куркою", "ingredients": [insertIds[5], insertIds[2]]},
]
# Видалення і створення таблиці dishes
if "dishes" in db.list_collection_names():
    db.drop_collection("dishes")
dishes = db.create_collection("dishes")
dishes.insert_many(data)

# Видалення і створення таблиці orders
if "orders" in db.list_collection_names():
    db.drop_collection("orders")
dishes = db.create_collection("orders")
