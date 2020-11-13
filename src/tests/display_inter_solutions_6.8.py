"""Solves an optimization problem and displays all intermediate solutions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model


# You need to subclass the cp_model.CpSolverSolutionCallback class.
class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables):
    self.__variables = variables
    self.__solution_count = 0

  def NewSolution(self):
    print('Solution %i' % self.__solution_count)
    print('  objective value = %i' % self.ObjectiveValue())
    for v in self.__variables:
      print('  %s = %i' % (v, self.Value(v)), end=' ')
    print()
    self.__solution_count += 1

  def SolutionCount(self):
    return self.__solution_count


def MinimalCpSatPrintIntermediateSolutions():
  """Showcases printing intermediate solutions found during search."""
  # Creates the model.
  model = cp_model.CpModel()
  # Creates the variables.
  num_vals = 3
  min_req = [1,1,1]
  x = model.NewIntVar(min_req[0], num_vals - 1, 'x')
  y = model.NewIntVar(min_req[1], num_vals - 1, 'y')
  z = model.NewIntVar(min_req[2], num_vals - 1, 'z')
  # Creates the constraints.
  # model.Add(x != y)
  model.Maximize(x + y + z)

  # Creates a solver and solves.
  solver = cp_model.CpSolver()
  solution_printer = VarArrayAndObjectiveSolutionPrinter([x, y, z])
  status = solver.SolveWithSolutionObserver(model, solution_printer)

  print('Status = %s' % solver.StatusName(status))
  print('Number of solutions found: %i' % solution_printer.SolutionCount())


MinimalCpSatPrintIntermediateSolutions()