class Dish(object):
    def __init__(self, name, ingredients, idx=None):
        self.idx = idx
        self.name = name
        self.ingredients = ingredients

    def __str__(self):
        return self.name

    def to_dict(self):
        """
        Повертає об'єкт у вигляді словника
        :return:
        """
        return {
            "idx": str(self.idx),
            "name": self.name,
            "ingredients": self.ingredients
        }
