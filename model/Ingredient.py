from bson import ObjectId


class Ingredient(object):
    def __init__(self, name, price, count, idx=None):
        self.idx = idx
        self.name = name
        self.price = price
        self.count = count

    def to_dict(self):
        """
        Повертає об'єкт у вигляді словника
        :return:
        """
        return {
            "idx": str(self.idx),
            "name": self.name,
            "price": self.price,
            "count": self.count
        }
