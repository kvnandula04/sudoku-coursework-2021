import numpy as np

# Rows and columns
elements = []
rows_columns_squares = []

for i in range(0, 9):
    row = []
    column = []
    for j in range(0, 9):
        elements.append((i, j))
        row.append((i, j))
        column.append((j, i))
    rows_columns_squares.append(row)
    rows_columns_squares.append(column)
    row = []
    column = []

# Squares
l = []
indices = []

def loop(xi, xj, indices, l):
    yi, yj = 0, 3
    while yi <= 6 and yj <= 9:
        for x in range(xi, xj):  
            for y in range(yi, yj):
                indices.append((x, y))
        rows_columns_squares.append(indices)
        indices = []
        yi += 3
        yj += 3
    
loop(0, 3, indices, l)
indices = []
loop(3, 6, indices, l)
indices = []
loop(6, 9, indices, l)
indices = []

# For each element, create a dictionary which contains a list of rows/columns/squares where that element exists
related_rcs = dict()
for element in elements:
    for list in rows_columns_squares:
        if element in list:
            if element in related_rcs:
                related_rcs[element].append(list)
            else:
                related_rcs[element] = [list]

# For each element, create a dictionary which contains a set of all the related elements(elements on the same row, column or square)
related_elements = dict()
for element in elements:
    related_elements[element] = set(sum(related_rcs[element],[])) - set([element])


digits = '123456789'

def check_validity(sudoku):
    # Check number of rows
    if len(sudoku) != 9:
        return False

    # Check number of columns
    for i in range(9):
        if len(sudoku[i]) != 9:
            return False
    
    # Check for repetitions in row, column or square
    for i in range(9):
        x, y = (i // 3) * 3, (i % 3) * 3
        if len(set(sudoku[i,:])) != 9 or len(set(sudoku[:,i])) != 9 or len(set(sudoku[x:x+3, y:y+3].flatten())) != 9:
            return False
    
    # Passes all tests
    return True
               
def get_possible_values(sudoku):
    possible_values = dict()
    
    # Initially set possible values to 123456789
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                possible_values[(i, j)] = digits
            
    # Filter the possible values based on values already provided
    for element in possible_values:
        for related_element in related_elements[element]:
            value = str(sudoku[related_element[0]][related_element[1]])
            if value in possible_values[element]:
                possible_values[element] = possible_values[element].replace(value, '')
    
    # Sort the dict in order of number of possible values
    return dict(sorted(possible_values.items(), key=lambda item: len(item[1])))

def backtrack(sudoku, possible_values):
    # Get next unfilled cell
    try:
        current_cell = next(iter(possible_values))
    except:
        return True
    
    for num in possible_values[current_cell]:
        # Try each value in list of possible values
        sudoku[current_cell[0]][current_cell[1]] = int(num)

        new_possible_values = possible_values.copy()
    
        # For each related element, if the related contains the same value that's just been assigned, remove it from its possible values
        for related in related_elements[current_cell]:
            if related in possible_values:
                if num in possible_values[related]:
                    new_possible_values[related] = new_possible_values[related].replace(num, '')
                    
        # Remove that value as it has been assigned
        del new_possible_values[current_cell]
        
        # Recursively try next values
        if backtrack(sudoku, dict(sorted(new_possible_values.items(), key=lambda item: len(item[1])))):
            return True
    
    # If none of the possible values work, there's no solution
    return False

def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    # Get possible values
    possible_values = get_possible_values(sudoku)
    
    # Check grid is valud and check for solution; return solution or grid of '-1's 
    if backtrack(sudoku, possible_values) and check_validity(sudoku):
        return np.array(sudoku)
    else:
        return np.full((9, 9), -1)