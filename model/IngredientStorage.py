from repository.IngredientRepository import IngredientRepository


class IngredientStorage:
    def __init__(self):
        ingredients = IngredientRepository().get_ingredients()
        self.storage = {}
        for i in ingredients:
            self.storage[i.idx] = i

    def to_update(self):
        ingredients = []
        for idx, ing in self.storage.items():
            ingredients.append((ing.count, ing.idx))
        return ingredients
