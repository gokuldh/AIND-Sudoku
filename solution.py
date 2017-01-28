"""
    Note : Most of the Code Except the Naked Twins Implementaion
    and the Addition of the Diagonal Units, was taken from the
    Udacity Course Material. As, the implementation by Udacity was better
    I Decided to use the Solutions provided by Udacity. :)
"""
#========== Initializations : Code taken from the Udacity Course Material ======!
assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#--- To get Diagonal Units ---
"Hardcoding the Diagonal Units Directly"
diagonal_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9',],['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
#-----------------------------
#---- Added Diagonal Units to the Unit List ---
unitlist = row_units + column_units + square_units + diagonal_units
#-----------------------------
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
#===============================================================================

#================= Naked Twins Strategy ========================================
def naked_twins(values):
    for cell in values:
        for peer in peers[cell]:
            if len(values[cell]) == 2 and values[cell] == values[peer]:
                values = remove_naked_twin(values, cell, peer, 0)
                values = remove_naked_twin(values, cell, peer, 1)
    return values
#===============================================================================

#================== Remove Naked Twins =========================================
def remove_naked_twin(values, cell, peer, i):
    for duplicate in units[cell][i]:
        for twin in values[cell]:
            if duplicate not in (peer,cell) and cell[i] == peer[i]:
                values[duplicate] = values[duplicate].replace(twin, '')
    return values
#===============================================================================


#==== Grid Values Function : Code taken from the Udacity Course Material =======!
def grid_values(grid):
    " This function Takes the values and return them in a Dictionary Form "
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))
#===============================================================================

#=========== Display Fucntion : Code taken from the Udacity Course Material ====!
def display(values):
    " Display the values as a 2-D grid "
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print
#===============================================================================

#========= Eliminate Fucntion : Code taken from the Udacity Course Material ====!
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values
#===============================================================================

#====== Only Choice Function : Code taken from the Udacity Course Material =====!
""" Note : Was stuck as the Pygame didn't work the Standard Udacity Code
    in the Course Material, Searched and got Help form the Slack Group that
    assign_value needs to be used :)"""
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values
#===============================================================================

#=== Reduce Puzzle Function : Code taken from the Udacity Course Material=======!
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
#===============================================================================

#======= Search Function : Code taken from the Udacity Course Material =========!
def search(values):
    "Using depth-first search and propagation, try all possible values."
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
#===============================================================================

#======= Solve Function ========================================================!
def solve(grid):
    "Given a grid, solve a sudoku puzzle."

    values = grid_values(grid)
    return search(values)
#===============================================================================

#===============================================================================!
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
#===============================================================================
