from repository.IngredientRepository import IngredientRepository


class IngredientService:
    ingredients = []

    def get_ingredients(self):
        """
        Повертає усі інгредієнти на складі
        :return:
        """
        self.ingredients = IngredientRepository().get_ingredients()

        return self.ingredients
