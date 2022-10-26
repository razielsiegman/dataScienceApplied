from traitlets.traitlets import enum
import random

columns = [] 
size = 4

def get_queens(size):
  columns = []
  row = 0
  while row < size:
    column=random.randrange(0,size)
    columns.append(column)
    row+=1
  return columns

def place_n_queens(size):
  columns.clear()
  row = 0
  while row < size:
      column=random.randrange(0,size)
      columns.append(column)
      row+=1

      
#dfs util methods

def place_in_next_row(column):
    columns.append(column)
 
def remove_in_current_row():
    if len(columns) > 0:
        return columns.pop()
    return -1
 
def next_row_is_safe(column):
    row = len(columns) 
    # check column
    for queen_column in columns:
        if column == queen_column:
            return False
 
    # check diagonal
    for queen_row, queen_column in enumerate(columns):
        if queen_column - queen_row == column - row:
            return False
 
    # check other diagonal
    for queen_row, queen_column in enumerate(columns):
        if ((size - queen_column) - queen_row
            == (size - column) - row):
            return False
    return True
 
 #hill climbing util methods
def conflict(row_a, column_a, row_b, column_b):
  if(row_a == row_b):
    return True
  if(column_a == column_b):
    return True
  if(abs(column_a - column_b) == abs(row_a - row_b)):
    return True
  return False

def highestConflict(columns): 
  highest_index = -1
  highest_count = 0
  for index_i, i in enumerate(columns):
    curr = 0
    for index_j, j in enumerate(columns):
      if index_i != index_j:
        if(conflict(index_i, i, index_j, j)):
          curr += 1
          if(curr >= highest_count):
            highest_count = curr
            highest_index = index_i
  return highest_index, highest_count

def conflictCount(columns, index):
  curr = 0
  for index_i, i in enumerate(columns):
    if index_i != index:
      if(conflict(index_i, i, index, columns[index])):
        curr += 1
  return curr

def british_museum(size):
  moves = 0
  iterations = 0
  while True:
    moves += size
    iterations += 1
    columns = get_queens(size)
    if highestConflict(columns)[1] == 0:
      return iterations, moves

def dfs(size):
    columns.clear()
    number_of_moves = 0 
    number_of_iterations = 0  
    row = 0
    column = 0
    # iterate over rows of board
    while True:
        #place queen in next row
        while column < size:
            number_of_iterations+=1
            number_of_moves+=1
            if next_row_is_safe(column):
                place_in_next_row(column)
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if (column == size or row == size):
            number_of_iterations+=1
            number_of_moves+=1
            # if board is full, we have a solution
            if row == size:
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            if (prev_column == -1): #I backtracked past column 1
                return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column 
    return number_of_iterations, number_of_moves

def hill_climbing(size):
  iterations = 1
  moves = size
  columns = get_queens(size)
  while True:
    highest_index, highest_count = highestConflict(columns)
    new_column = -1
    if(highest_count == 0):
      break
    for i in range(len(columns)):
      temp = columns.copy()
      temp[highest_index] = i
      if(conflictCount(columns, highest_index) > conflictCount(temp, highest_index)):
        columns = temp
        iterations += 1
        moves += 1
        new_column = 0
        break
    if(new_column == -1):
      columns = get_queens(size)
      iterations += 1
      moves += size
  return moves, iterations

def forward(size):
    columns.clear()
    number_of_moves = 0 
    number_of_iterations = 0  
    row = 0
    column = 0
    not_available = dict.fromkeys(range(size))
    for k in not_available:
      not_available[k] = []

    # iterate over rows of board
    while True:
        #place queen in next row
        while column < size:
            if column not in not_available.get(row):
                number_of_moves += 1
                number_of_iterations+=1
                #place_in_next_row(column)
                columns.append(column)
                for i in range(size):
                  for j in range(size):
                    if(conflict(row, column, i, j)):
                      mylist = not_available[i]
                      mylist.append(j)
                row += 1
                column = 0
                break
            else:
                column += 1
        # if I could not find an open column or if board is full
        if (column == size or row == size):
            # if board is full, we have a solution
            if row == size:
                return number_of_iterations, number_of_moves
            # I couldn't find a solution so I now backtrack
            prev_column = remove_in_current_row()
            not_available = dict.fromkeys(range(size))
            for k in not_available:
              not_available[k] = []
            for index_i, i in enumerate(columns):
                for j in range(size):
                  for k in range(size):
                    if(conflict(index_i, i, j, k)):
                      mylist = not_available[j]
                      mylist.append(k)


            if (prev_column == -1): #I backtracked past column 1
                 return number_of_iterations, number_of_moves
            # try previous row again
            row -= 1
            # start checking at column = (1 + value of column in previous row)
            column = 1 + prev_column 
    return number_of_iterations, number_of_moves

british_iter = 0
british_moves = 0
british_iter_min = 1000000
british_iter_max = 0
british_moves_min = 10000000
british_moves_max = 0
for i in range(10):
  iterations, moves = british_museum(8)
  if moves < british_moves_min:
    british_moves_min = moves
  if iterations < british_iter_min:
    british_iter_min = iterations
  if moves > british_moves_max:
    british_moves_max = moves
  if iterations > british_iter_max:
    british_iter_max = iterations
  british_iter += iterations
  british_moves += moves
british_iter = british_iter/10
british_moves = british_moves/10
print('british iterations average', british_iter)
print('british iterations min', british_iter_min)
print('british iterations max', british_iter_max)
print('british moves average', british_moves)
print('british moves min', british_moves_min)
print('british moves max', british_moves_max)

dfs_iter = 0
dfs_moves = 0
dfs_iter_min = 1000000
dfs_iter_max = 0
dfs_moves_min = 10000000
dfs_moves_max = 0
for i in range(10):
  iterations, moves = dfs(8)
  if moves < dfs_moves_min:
    dfs_moves_min = moves
  if iterations < dfs_iter_min:
    dfs_iter_min = iterations
  if moves > dfs_moves_max:
    dfs_moves_max = moves
  if iterations > dfs_iter_max:
    dfs_iter_max = iterations
  dfs_iter += iterations
  dfs_moves += moves
dfs_iter = dfs_iter/10
dfs_moves = dfs_moves/10
print('dfs iterations average', dfs_iter)
print('dfs iterations min', dfs_iter_min)
print('dfs iterations max', dfs_iter_max)
print('dfs moves average', dfs_moves)
print('dfs moves min', dfs_moves_min)
print('dfs moves max', dfs_moves_max)


forward_iter = 0
forward_moves = 0
forward_iter_min = 1000000
forward_iter_max = 0
forward_moves_min = 10000000
forward_moves_max = 0
for i in range(10):
  iterations, moves = forward(8)
  if moves < forward_moves_min:
    forward_moves_min = moves
  if iterations < forward_iter_min:
    forward_iter_min = iterations
  if moves > forward_moves_max:
    forward_moves_max = moves
  if iterations > forward_iter_max:
    forward_iter_max = iterations
  forward_iter += iterations
  forward_moves += moves
forward_iter = forward_iter/10
forward_moves = forward_moves/10
print('forward iterations average', forward_iter)
print('forward iterations min', forward_iter_min)
print('forward iterations max', forward_iter_max)
print('forward moves average', forward_moves)
print('forward moves min', forward_moves_min)
print('forward moves max', forward_moves_max)



hill_climbing_iter = 0
hill_climbing_moves = 0
hill_climbing_iter_min = 1000000
hill_climbing_iter_max = 0
hill_climbing_moves_min = 10000000
hill_climbing_moves_max = 0
for i in range(10):
  iterations, moves = hill_climbing(8)
  if moves < hill_climbing_moves_min:
    hill_climbing_moves_min = moves
  if iterations < hill_climbing_iter_min:
    hill_climbing_iter_min = iterations
  if moves > hill_climbing_moves_max:
    hill_climbing_moves_max = moves
  if iterations > hill_climbing_iter_max:
    hill_climbing_iter_max = iterations
  hill_climbing_iter += iterations
  hill_climbing_moves += moves
hill_climbing_iter = hill_climbing_iter/10
hill_climbing_moves = hill_climbing_moves/10
print('hill_climbing iterations average', hill_climbing_iter)
print('hill_climbing iterations min', hill_climbing_iter_min)
print('hill_climbing iterations max', hill_climbing_iter_max)
print('hill_climbing moves average', hill_climbing_moves)
print('hill_climbing moves min', hill_climbing_moves_min)
print('hill_climbing moves max', hill_climbing_moves_max)



"""
SAMPLE RESULTS

british iterations 133650.4
british iterations min 10833
british iterations max 333253
british moves 1069203.2
british moves min 86664
british moves max 2666024

forward iterations average 113.0
forward iterations min 113
forward iterations max 113
forward moves average 113.0
forward moves min 113
forward moves max 113

dfs iterations average 982.0
dfs iterations min 982
dfs iterations max 982
dfs moves average 982.0
dfs moves min 982
dfs moves max 982

hill_climbing iterations average 244.3
hill_climbing iterations min 13
hill_climbing iterations max 759
hill_climbing moves average 102.9
hill_climbing moves min 6
hill_climbing moves max 318
"""

