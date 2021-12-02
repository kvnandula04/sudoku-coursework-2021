from copy import deepcopy
import numpy as np

elements = []
rows_columns_squares = []

# add new comment for the bantzzz

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

# For each element, create a dictionary called related_rcs which contains a list of rows/columns/squares where that element exists
related_rcs = dict()
for element in elements:
    for list in rows_columns_squares:
        if element in list:
            if element in related_rcs:
                related_rcs[element].append(list)
            else:
                related_rcs[element] = [list]

# For each element, create a dictionary related_elements which contains a set of all the related elements(elements on the same row, column or square)
related_elements = dict()
for element in elements:
    related_elements[element] = set(sum(related_rcs[element],[])) - set([element])

digits = '123456789'

def get_possible_values(sudoku):
    possible_values = dict()
    for element in elements:
        possible_values[element] = digits

    for key, value in get_sudoku_values(sudoku).items():
        if value in digits and not set_value(possible_values, key, value):
            return False

    return possible_values

def get_sudoku_values(sudoku):
    chars = []
    for i in range(0, 9):
        for j in range(0, 9):
            digit = str(sudoku[i][j])
            if digit in digits or digit == '0':
                chars.append(digit)
    
    return dict(zip(elements, chars))

def set_value(possible_values, key, value):
    rem_possible_values = possible_values[key].replace(value, '')
    if all(filter(possible_values, key, value2) for value2 in rem_possible_values):
        return possible_values
    else:
        return False

def filter(possible_values, key, value):
    if value not in possible_values[key]:
        return possible_values
    
    possible_values[key] = possible_values[key].replace(value, '')

    # if the length of the possible values is 1, then it's the last possible value that cell can have
    if len(possible_values[key]) == 0:
        return False
    elif len(possible_values[key]) == 1:
        value2 = possible_values[key]
        if not all(filter(possible_values, related_element_key, value2) for related_element_key in related_elements[key]):
            return False

    for related in related_rcs[key]:
        locations_of_val = [key for key in related if value in possible_values[key]]
        
        if len(locations_of_val) == 0:
            return False
        elif len(locations_of_val) == 1:
            if not set_value(possible_values, locations_of_val[0], value):
                return False

        return possible_values

def solve(sudoku): 
    return search(get_possible_values(sudoku))

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: 
            return e
    return False

def search(possible_values):
    if possible_values is False:
        return False # Failed earlier

    if all(len(possible_values[element]) == 1 for element in elements): 
        return possible_values

    key, val = min((len(possible_values[element]), element) for element in elements if len(possible_values[element]) > 1)

    return some(search(set_value(deepcopy(possible_values), val, value))
        for value in possible_values[val])


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
    try:
        solution_dict = solve(sudoku)

        for i in range(0, 9):
            for j in range(0, 9):
                if sudoku[i][j] == 0:
                    sudoku[i][j] = int(solution_dict[(i, j)])

        return np.array(sudoku)
    except:
        return np.full((9, 9), -1)

print(sudoku_solver([[0,0,0,3,2,8,7,1,9]
,[3,8,7,9,1,6,4,5,2]
,[2,9,1,4,5,7,6,3,8]
,[5,6,3,2,9,1,8,7,4]
,[0,7,8,6,4,5,1,2,3]
,[1,2,4,8,7,3,5,9,6]
,[7,3,9,5,6,4,2,8,1]
,[8,5,6,1,3,2,9,0,7]
,[4,1,2,7,8,9,3,6,5]]))