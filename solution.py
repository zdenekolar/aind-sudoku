assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins_alternative(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for unit in unitlist:
        for box in unit:
            if len(values[box]) == 2:
                instances = [b for b in unit if values[b] == values[box]]                
                if len(instances) == 2:                                        
                    for digit in values[box]:
                        occurences = [b for b in unit if len(values[b]) > 2]
                        for o in occurences:
                            assign_value(values, o, values[o].replace(digit, ''))                            
                 
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    display(values)
    for box in boxes:
        if len(values[box]) == 2:            
            dplaces = [b for b in peers[box] if values[box] == values[b]]                        
            if len(dplaces) == 1:                
                for i in list(set(peers[dplaces[0]]) & set(peers[box])):
                    for d in values[box]:                
                        assign_value(values, i, values[i].replace(d,''))                
    return values

def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    
    Args:
        A(list): a list
        B(list): a list
        
    Returns:
        the cross product of A and B
    
    """
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

diag_units = [[(rows[i]+cols[i]) for i in range(0, len(rows))]]
diag_units.append([(rows[i]+cols[len(cols)-i-1]) for i in range(0, len(rows))])

unitlist = row_units + column_units + square_units + diag_units
# Generate units that contain boxes
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# Generate a list of peers of each box, subtract boxes
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    
    assert len(grid) == 81
    dic = dict(zip(cross(rows, cols), grid))
    
    # Assign '123456789' for 
    empty = '123456789'    
    empty_boxes = [box for box in dic.keys() if dic[box] == '.']
    
    for box in empty_boxes:
        dic[box] = empty
    return dic

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    
    width = 1 + max(len(values[s]) for s in values.keys())
    line = '+'.join((['-'*width*3])*3)
    
    for r in rows:                
        print(''.join(values[r+c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
            
            

def eliminate(values):
    '''
    If there is a single value, eliminate it from the peers of the box.
    
    Args:
        values(dict)
    Returns
        values(dict)
    
    '''
    solved_values = [box for box in values.keys() if len(values[box] ) == 1]
    for box in solved_values:
        value = values[box]        
        for peer in peers[box]:
#            values[peer] = values[peer].replace(value, '')
            assign_value(values, peer, values[peer].replace(value, ''))
            
        
    return values
    

def only_choice(values):
    '''
    Remove only occurence of a value from its peers in unit
    
    Args:
        values(dict)
    Returns
        values(dict)
    '''
    digits = '123456789'
    for unit in unitlist:
        for digit in digits:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:                
#                values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    '''
    Iterate eliminate and only_choice functions until solution is found
    or the process stalls.
    
    Args:
        values(dict)
    Returns
        values(dict)
    '''
    stalled = False
    i = 0
    while not stalled:
        i+=1
        print('Iteration {}'.format(i))
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    '''
    Use depth-first search and propagation and create a search tree to solve the sudoku.
    
    '''    
    values = reduce_puzzle(values)
    # End condition, no success
    if values == False:
        return False
    # End consition, we found a solution
    if all(len(values[s]) == 1 for s in values.keys()):
        return values
    # Neither of the above cases, we try to assign one value from values[s] to the
    # box with minimum number of possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    grid_dict = grid_values(grid)
    values = search(grid_dict)

    return values
    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'     
    solve(diag_sudoku_grid)    

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
