class ResultReceiver:

    def __init__(self, data, data_evaluator, food) -> None:
        self.data = data
        self.data_evaluator = data_evaluator
        self.food = food


    def get_result(self, i):
        result = ''
        price = 0
        num_nutrients = len(self.data.datas[i]) - 3
        nutrients = [0] * num_nutrients
        for i in range(0, self.data.num_data):
            price += self.food[i].solution_value()
            for nutrient in range(0, num_nutrients):
                nutrients[nutrient] += self.data_evaluator(i, nutrient + 3) * self.food[i].solution_value()
            if self.food[i].solution_value() > 0:
                # print("[###] ", self.food[i].index())
                result += "%s = %f\n" % (self.data_evaluator(i, 0), self.food[i].solution_value())
        result += 'Optimal price: $%.2f' % (price)
        return result
