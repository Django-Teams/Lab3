class Order(object):
    def __init__(self, name, sum, dishes, idx=None):
        self.idx = idx
        self.name = name
        self.sum = sum
        self.dishes = dishes
