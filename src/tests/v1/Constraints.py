from .models import Nutrients


class DataEvaluator:
    """Creates Data evaluator for Price per Commodity and Vendor"""


    def __init__(self, data) -> None:
        self._data = data.datas


    def data_evaluator(self, vendor, commodity):
        return self._data[vendor][commodity]


class NutrientEvaluator:
    """Creates Evaluator for List of Drugs needed"""


    def __init__(self, nutrients: Nutrients) -> None:
        self._nutrients = nutrients.nutrients


    def nutrient_evaluator(self, nutrient, requirement):
        del requirement
        return self._nutrients[nutrient]
