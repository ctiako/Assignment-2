# CS305 Park University
# Assignment #2
# Solving Sudoku as a CSP

from itertools import product

# Define the Variable class
class Variable:
    def __init__(self, name, domain, position):
        self.name = name
        self.domain = domain
        self.position = position

    def __repr__(self):
        return f"Variable({self.name}, {self.domain})"

# Define the Constraint class
class Constraint:
    def __init__(self, name, variables, constraint_func):
        self.name = name
        self.variables = variables
        self.constraint_func = constraint_func

    def is_satisfied(self, assignment):
        values = [assignment.get(var) for var in self.variables]
        if None in values:
            return True  # Ignore if any variable is unassigned
        return self.constraint_func(*values)

# Define the CSP class
class CSP:
    def __init__(self, name, variables, constraints):
        self.name = name
        self.variables = {var.name: var for var in variables}
        self.constraints = constraints
        self.domains = {var.name: var.domain.copy() for var in variables}

    def is_consistent(self, var, assignment):
        for constraint in self.constraints:
            if var in [v.name for v in constraint.variables]:
                if not constraint.is_satisfied(assignment):
                    return False
        return True

    def backtrack(self, assignment={}):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned_vars = [v for v in self.variables.values() if v.name not in assignment]
        first = unassigned_vars[0]
        
        for value in self.domains[first.name]:
            local_assignment = assignment.copy()
            local_assignment[first.name] = value
            
            if self.is_consistent(first.name, local_assignment):
                result = self.backtrack(local_assignment)
                if result is not None:
                    return result

        return None

# Function to convert puzzle text to variable dictionary
def puzzle_text_to_var_dict(txt):
    """Converts a textual representation of a sudoku board to a dictionary of variables."""
    variables = {}
    row, col = 1, 1
    for c in txt:
        if c in '123456789':
            variables[(row, col)] = Variable(f'[{row},{col}]', {int(c)}, (row, col))
        elif c == '?':
            variables[(row, col)] = Variable(f'[{row},{col}]', set(range(1, 10)), (row, col))
        if c in '123456789?':
            col = (col % 9) + 1
            if col == 1: 
                row += 1
    return variables

# Function to print the solution
def print_solution(solution, variables):
    """Prints out variable assignments as a sudoku board for a CSP sudoku solution."""
    for r in range(1, 10):
        print(" ", end="")
        for c in range(1, 10):
            print(solution[variables[(r, c)].name], end="")
            if c % 3 == 0 and c < 9:
                print(" | ", end="")
            else:
                print(" ", end="")
        if r % 3 == 0 and r < 9:
            print("\n-------+-------+------")
        else:
            print("")

# Function to enforce the all-different constraint
def all_diff(variables):
    """Returns a Constraint that enforces all variables to have different values."""
    def constraint_function(*values):
        return len(values) == len(set(values))
    return Constraint("AllDiff", variables, constraint_function)

# Function to create Sudoku constraints
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
            block_vars = [variables[(br + r, bc + c)] for r, c in product(range(3), repeat=2)]
            constraints.append(all_diff(block_vars))

    return constraints

# Main function
def main():
    puzzle_text = """ 
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
    
    variables = puzzle_text_to_var_dict(puzzle_text)
    constraints = create_sudoku_constraints(variables)
    sudoku_csp = CSP("Sudoku", variables.values(), constraints)
    solution = sudoku_csp.backtrack()

    if solution:
        print("Solution:")
        print_solution(solution, variables)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()


Solution:
 5 3 4 | 6 7 8 | 9 1 2 
 6 7 2 | 1 9 5 | 3 4 8 
 1 9 8 | 3 4 2 | 5 6 7 
-------+-------+------
 8 5 9 | 7 6 1 | 4 2 3 
 4 2 1 | 8 1 3 | 1 9 1 
 7 1 3 | 9 2 4 | 8 5 6 
-------+-------+------
 9 6 1 | 5 3 7 | 2 8 4 
 2 8 7 | 4 1 9 | 6 3 5 
 3 4 5 | 2 8 6 | 1 7 9 
