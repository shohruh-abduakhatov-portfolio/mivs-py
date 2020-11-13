class Nutrient:
    """Stores Required Drugs"""


    def __init__(self, nutrient_requirements) -> None:
        self._nutrients = nutrient_requirements


    @property
    def nutrients(self):
        return self._nutrients


    @property
    def num_nutrients(self):
        return len(self._nutrients)
