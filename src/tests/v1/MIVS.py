from ortools.linear_solver import pywraplp

from src.Constraints import DataEvaluator, NutrientEvaluator
from src.ResultReceiver import ResultReceiver
from src.models.Data import Data
from src.models.Nutrients import Nutrient


async def generate_data(data, nutriment):
    """Generates Sample Data"""
    data = Data(*data)
    data_evaluator = DataEvaluator(data).data_evaluator
    # Nutrient minimums.
    nutrients = Nutrient(nutriment)
    nutrient_evaluator = NutrientEvaluator(nutrients).nutrient_evaluator
    return data, data_evaluator, nutrients, nutrient_evaluator


async def main(**kwargs):
    # Commodity, Unit, 1939 price (cents), Calories, Protein (g), Calcium (g), Iron (mg),
    # Vitamin A (IU), Thiamine (mg), Riboflavin (mg), Niacin (mg), Ascorbic Acid (mg)
    data, data_evaluator, nutrients, nutrient_evaluator = await generate_data(kwargs['data'], kwargs['nutrient'])

    # Instantiate a Glop solver, naming it SolveStigler.
    solver = pywraplp.Solver('SolveStigler', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    # Declare an array to hold our nutritional data.
    food = [[]] * data.num_data
    # Objective: minimize the sum of (price-normalized) foods.
    objective = solver.Objective()
    for i in range(0, data.num_data):
        food[i] = solver.NumVar(0.0, solver.infinity(), data_evaluator(i, 0))
        objective.SetCoefficient(food[i], 1)
    objective.SetMinimization()

    # Create the constraints, one per nutrient.
    constraints = [0] * nutrients.num_nutrients
    for i in range(0, nutrients.num_nutrients):
        constraints[i] = solver.Constraint(nutrient_evaluator(i, 1), solver.infinity())
        # print(">>>", constraints[i].lb())
        for j in range(0, data.num_data):
            constraints[i].SetCoefficient(food[j], data_evaluator(j, i + 3))
    # Solve!
    status = solver.Solve()
    if status == solver.OPTIMAL:
        # Display the amounts (in dollars) to purchase of each food.
        result = ResultReceiver(data, data_evaluator, food).get_result(i)
    else:  # No optimal solution was found.
        if status == solver.FEASIBLE:
            result = 'A potentially suboptimal solution was found.'
        else:
            result = 'The solver could not solve the problem.'
    # print(result)
    return result


if __name__ == '__main__':
    main()
