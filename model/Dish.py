class Dish(object):
    def __init__(self, name, ingredients, idx=None):
        self.idx = idx
        self.name = name
        self.ingredients = ingredients

    def __str__(self):
        return self.name
