class Order(object):
    def __init__(self, name, sum, dishes, idx=None):
        self.idx = idx
        self.name = name
        self.sum = sum
        self.dishes = dishes

    def to_dict(self):
        """
        Повертає об'єкт у вигляді словника
        :return:
        """
        return {
            "idx": str(self.idx),
            "name": self.name,
            "sum": self.sum,
            "dishes": self.dishes
        }
