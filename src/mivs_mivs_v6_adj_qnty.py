from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from enum import Enum

from ortools.sat.python import cp_model
import numpy as np


# You need to subclass the cp_model.CpSolverSolutionCallback class.
class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    NUM_TRIALS = 6


    def __init__(self, variables, data):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        # data
        self._var_qnty_list_title = []
        self._product = data.get("_product", [])
        self._req_qnty = data.get("_req_qnty", [])
        self._input_capital = data.get("_input_capital", [])
        self._cash = data.get("_cash", [])
        self._perech = data.get("_perech", [])
        self._supplier = data.get("_supplier", [])
        self._prices_title = data.get("_prices_title", [])
        self._kwargs = data.get("kwargs", {})
        self._status = cp_model.UNKNOWN
        self._solution_trial = data.get("solution_trial", self.NUM_TRIALS)
        self._solution = {}
        # **kwargs
        # self._min_sum_per_supplier = data.get("min_sum_per_supplier", [])
        # self._discount_threshold = data.get("discount_threshold", [])
        # self._discount_percent = data.get("discount_percent", [])
        # self._supp_overhead = data.get("supp_overhead", [])


    def on_solution_callback(self):
        print('Solution %i' % self.__solution_count)
        print('  objective value = %i' % self.ObjectiveValue())
        _req_qnty = []
        _var_qnty_list_title = []
        if self._solution_trial >= self.__solution_count and self._status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            for v in self.__variables:
                v_val = self.Value(v)
                print('  %s = %i' % (v, v_val), end=' ')
                _req_qnty.append(v_val)
                _var_qnty_list_title.append(v)
            self._req_qnty = _req_qnty
            self._var_qnty_list_title = _var_qnty_list_title
            del _req_qnty, _var_qnty_list_title
            response = self.calc_optimal_prices()
            print("total cost: ", response.get('total_cost'))
            print()
            if response['status'] == cp_model.OPTIMAL:
                if response.get('total_cost') < self._solution.get('total_cost') or self._solution == {}:
                    self._solution = response
                    self.__solution_count += 1
                    if self._solution_trial == self.__solution_count:
                        self._status = response['status']


    async def calc_optimal_prices(self):
        return {"status": cp_model.UNKNOWN}
        from src import mc_mivs_v6_wire100 as mc_mivs
        result = await mc_mivs.main(self._product,
                                    self._req_qnty,
                                    self._input_capital,
                                    self._cash,
                                    self._perech,
                                    self._supplier,
                                    self._prices_title,
                                    preds=self._kwargs['preds'],
                                    min_sum_per_supplier=self._kwargs['_min_sum_per_supplier'],
                                    discount_threshold=self._kwargs['_discount_threshold'],
                                    discount_percent=self._kwargs['_discount_percent'],
                                    supp_overhead=self._kwargs['_supp_overhead'])
        return result


    def solution_count(self):
        return self.__solution_count


def get_qnty_required(min_sum_per_supplier, wires, _input_capital, **kwargs):
    _wires = np.where(wires == _input_capital, 0, wires)
    qnty = np.ceil(min_sum_per_supplier[None, :] / _wires)
    qnty[qnty == np.inf] = 0
    qnty = np.max(qnty, axis=1).flatten().astype('int')
    _req_qnty = np.array(kwargs.get('req_qnty', []))
    mask = qnty < _req_qnty
    np.putmask(qnty, mask, _req_qnty[mask])
    np.putmask(_req_qnty, mask, (_req_qnty[mask] * 1.01).astype('int'))
    return qnty, _req_qnty


def main(_product,
         _req_qnty,
         _input_capital,
         _cash,
         _perech,
         _supplier,
         _prices_title,
         **kwargs):
    data = {
        "_product": _product,
        "_req_qnty": _req_qnty,
        "_input_capital": _input_capital,
        "_cash": _cash,
        "_perech": _perech,
        "_supplier": _supplier,
        "_prices_title": _prices_title,
        "kwargs": kwargs
    }

    """Showcases printing intermediate solutions found during search."""
    # Creates the model.
    model = cp_model.CpModel()
    fmt_qnty = "qnty_%s"
    qnty_adj, _req_qnty = get_qnty_required(np.array(kwargs.get("min_sum_per_supplier")),
                                            np.array(kwargs.get("preds").get("pred100")),
                                            _input_capital, req_qnty=_req_qnty)
    """lengths"""
    num_prod = len(_product)

    """empty cp.sat vars"""
    var_qnty_list = np.full(shape=(num_prod), fill_value=model.NewIntVar(0, 0, '_'))

    """declaring vars"""
    for p in range(num_prod):  # per drug
        var_qnty_list[p] = model.NewIntVar(int(qnty_adj[p]), int(_req_qnty[p]), fmt_qnty % (p))

    """adding constraints"""
    for p in range(num_prod):  # per drug
        model.Add(var_qnty_list[p] >= _req_qnty[p])

    model.Minimize(cp_model._SumArray(var_qnty_list))
    solver = cp_model.CpSolver()
    solution_printer = VarArrayAndObjectiveSolutionPrinter(var_qnty_list, data=data)
    status = solver.SolveWithSolutionObserver(model, solution_printer)
    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: %i' % solution_printer.solution_count())


if __name__ == '__main__':
    main()

# SolveAndPrintIntermediateSolutionsSampleSat()
