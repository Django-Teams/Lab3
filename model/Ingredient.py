class Ingredient(object):
    def __init__(self, name, price, count, idx=None):
        self.idx = idx
        self.name = name
        self.price = price
        self.count = count
