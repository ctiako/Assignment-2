# CS305 Park University
# Assignment #2 Starter Code
# Solving Sudoku as a CSP
# By Cyrille Tekam Tiako
# 22 Aug 2024

from cspProblem import Variable, CSP, Constraint
from cspDFS import dfs_solve1    
from operator import lt, ne, eq, gt

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
    """Converts a textual representation of a sudoku board to a dictionary of
    variables with (row, col) tuples as keys."""
    variables = dict()
    row, col = 1, 1
    for c in txt:
        if c >= '1' and c <= '9':
            variables[(row, col)] = Variable(f'[{row},{col}]', {int(c)}, (row, col))
            col = (col % 9) + 1
            if col == 1: 
                row = (row % 9) + 1
        elif c == '?':
            variables[(row, col)] = Variable(f'[{row},{col}]', set(range(1, 10)), (row, col))
            col = (col % 9) + 1
            if col == 1: 
                row = (row % 9) + 1
    return variables
      
      
def print_solution(sol, variables):
    """Prints out variable assignments as a sudoku board for a CSP sudoku solution."""
    for r in range(1, 10):
        print(" ", end="")
        for c in range(1, 10):
            print(sol[variables[(r, c)]], end="")
            if c % 3 == 0 and c < 9:
                print(" | ", end="")
            else:
                print(" ", end="")
        if r % 3 == 0 and r < 9:
            print("\n-------+-------+------")
        else:
            print("")


def all_diff(variables):
    """Returns a Constraint that enforces all variables to have different values."""
    def constraint_function(*values):
        return len(values) == len(set(values))
    return Constraint("AllDiff", variables, constraint_function)


def create_sudoku_constraints(variables): 
    constraints = []
    
    # Row constraints
    for r in range(1, 10):
        row_vars = [variables[(r, c)] for c in range(1, 10)]
        constraints.append(all_diff(row_vars))
    
    # Column constraints
    for c in range(1, 10):
        col_vars = [variables[(r, c)] for r in range(1, 10)]
        constraints.append(all_diff(col_vars))
    
    # Block constraints
    for br in range(1, 10, 3):
        for bc in range(1, 10, 3):
            block_vars = [variables[(br + r, bc + c)] for r in range(3) for c in range(3)]
            constraints.append(all_diff(block_vars))
    
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


