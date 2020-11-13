"""Code sample that solves a model and displays all solutions."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self, variables):
    super().__init__()
    self.__variables = variables
    self.__solution_count = 0

  def NewSolution(self):
    self.__solution_count += 1
    for v in self.__variables:
      print('%s=%i' % (v, self.Value(v)), end=' ')
    print()

  def SolutionCount(self):
    return self.__solution_count


def MinimalSatSearchForAllSolutions():
  """Showcases calling the solver to search for all solutions."""
  # Creates the model.
  model = cp_model.CpModel()
  # Creates the variables.
  num_vals = 3
  x = model.NewIntVarFromDomain(cp_model.Domain.FromIntervals([[0, 0], [num_vals-1, num_vals-1]]), name='x')
  y = model.NewIntVarFromDomain(cp_model.Domain.FromIntervals([[0, 0], [num_vals-1, num_vals-1]]), name='y')
  z = model.NewIntVarFromDomain(cp_model.Domain.FromIntervals([[0, 0], [num_vals-1, num_vals-1]]), name='z')
  # Create the constraints.
  # model.Add(x != y)

  # Create a solver and solve.
  solver = cp_model.CpSolver()
  solution_printer = VarArraySolutionPrinter([x, y, z])
  status = solver.SearchForAllSolutions(model, solution_printer)
  # solver = cp_model.CpSolver()
  # solver.parameters.num_search_workers = 2
  # solver.parameters.max_time_in_seconds = 60.
  # status = solver.Solve(model)
  # print('  - status          : %s' % solver.StatusName(status), '(code:', status, ')')
  # print('  - conflicts       : %i' % solver.NumConflicts())
  # print('  - branches        : %i' % solver.NumBranches())
  # print('  - wall time       : %f ms' % solver.WallTime())
  #
  # print("x = ", solver.Value(x))
  # print("y = ", solver.Value(y))
  # print("z = ", solver.Value(z))



MinimalSatSearchForAllSolutions()