# CS305 Park University
# Assignment #2 Starter Code
# Solving Sudoku as a CSP

from cspProblem import Variable, CSP, Constraint
from cspDFS import dfs_solve1    
from operator import lt,ne,eq,gt

# Attention:
# To test your code, add ?'s where you want to have the CSP solver determine
# the variable value. The search-based approach isn't very efficient, so 
# adding too many may make the solver spend a very long time searching for 
# a solution. Consider how you could make this more efficient by manipulating
# the domains in the puzzle_text_to_var function below or by using a more
# sophisticated CSP solving algorithm from the optional reading in Ch. 4.
#
# The code you have to write for this assignment is further below. 

puzzle_text1 = """ 
 5 3 4 | 6 7 8 | 9 1 2 
 6 7 2 | 1 9 5 | 3 4 8 
 1 9 8 | 3 4 2 | 5 6 7
-------+-------+------ 
 8 5 9 | 7 6 1 | 4 2 3
 4 2 ? | 8 ? 3 | ? 9 1 
 7 1 3 | 9 2 4 | 8 5 6 
-------+-------+------ 
 9 6 1 | 5 3 7 | 2 8 4 
 2 8 7 | 4 1 9 | 6 3 5 
 3 4 5 | 2 8 6 | 1 7 9
"""


def puzzle_text_to_var_dict(txt):
  """converts a textual representation of a sudoku board to a dictionary of
  variables with (row, col) tuples as keys"""
  variables = dict()
  row, col = 1, 1
  for c in txt:
    if c >= '1' and c <= '9':
      variables[row, col] = Variable('['+str(row)+','+str(col)+']', {int(c)}, (row, col))
      col = (col % 9) + 1
      if col == 1: 
        row = (row % 9) + 1
    if c == '?':
      variables[row, col] = Variable('['+str(row)+','+str(col)+']', set(range(1,10)), (row, col))
      col = (col % 9) + 1
      if col == 1: 
        row = (row % 9) + 1
  return variables
      
      
def print_solution(sol, variables):
  """prints out variable assignments as a sudoku board for a CSP sudoku solution"""
  for r in range(1,10):
    print(" ", end="")
    for c in range(1,10):
      print(sol[variables[r,c]], end="")
      if c % 3 == 0 and c < 9:
        print(" | ", end="")
      else:
        print(" ", end="")
    if r % 3 == 0 and r < 9:
      print("\n-------+-------+------")
    else:
      print("")
  
def create_sudoku_constraints(variables): 
  constraints = []
  # TODO: Create Constraint objects and append them to the list of 
  # constraints that this function returns. You will need to create 
  # enough constraints to ensure no variables on the sudoku board have
  # a value assignment that is inconsistent with the rules of sudoku. 
  # Specifically: 
  #  1) Every variable in a row of the puzzle must have unique values assigned
  #     from the domain {1, 2, ... 9}
  #  2) Every variable in a column of the puzzle must have unique values 
  #     assigned from the domain {1, 2, ... 9}
  #  3) Every variable in a block (see segmented portion of the strings above)
  #     of the puzzle must have unique values assigned from the 
  #     domain {1, 2, ... 9}
  
  # hint 1: you will want to use loops, generators, or comprehensions to
  # create the constraints. There should be at least 27 of them, if not more,
  # depending on your approach. 

  # hint 2: you may want to create a custom function to use in your constraints 
  # to enforce the uniqueness-among-variables constraint

  return constraints

def main():
  puzzle_text = puzzle_text1
  variables = puzzle_text_to_var_dict(puzzle_text)
  constraints = create_sudoku_constraints(variables)
  print("Input Puzzle: ")
  print(puzzle_text)
  print("Solution: ")
  sudoku1 = CSP("sudoku", variables.values(), constraints)
  sol = dfs_solve1(sudoku1)
  print_solution(sol, variables)
  
if __name__ == '__main__':
  main()
