from repository.IngredientRepository import IngredientRepository


class IngredientService:
    ingredients = []

    def get_ingredients(self):
        """
        Return all ingredients in storage
        :return:
        """
        self.ingredients = IngredientRepository().get_ingredients()

        return self.ingredients

    def change_count(self, ):
        pass
