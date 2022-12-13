import copy
import numpy as np
import random

# # # # # # # # # # # # # # global values  # # # # # # # # # # # # # #
ROW_COUNT = 6
COLUMN_COUNT = 7

RED_CHAR = 'X'
BLUE_CHAR = 'O'


EMPTY = 0
RED_INT = 1
BLUE_INT = 2


# # # # # # # # # # # # # # functions definitions # # # # # # # # # # # # # #

def create_board():
    """creat empty board for new game"""
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


def drop_chip(board, row, col, chip):
    """place a chip (red or BLUE) in a certain position in board"""
    board[row][col] = chip

def is_valid_location(board, col):
    """check if a given column in the board has a room for extra dropped chip"""
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    """assuming column is available to drop the chip,
    the function returns the lowest empty row  """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """print current board with all chips put in so far"""
    # print(np.flip(board, 0))
    print(" 1 2 3 4 5 6 7 \n" "|" + np.array2string(np.flip(np.flip(board, 1)))
          .replace("[", "").replace("]", "").replace(" ", "|").replace("0", "_")
          .replace("1", RED_CHAR).replace("2", BLUE_CHAR).replace("\n", "|\n") + "|")

def game_is_won(board, chip):
    """check if current board contain a sequence of 4-in-a-row of in the board
     for the player that play with "chip"  """

    winning_Sequence = np.array([chip, chip, chip, chip])
    # Check horizontal sequences
    for r in range(ROW_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[r, :]))):
            return True
    # Check vertical sequences
    for c in range(COLUMN_COUNT):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board[:, c]))):
            return True
    # Check positively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, board.diagonal(offset)))):
            return True
    # Check negatively sloped diagonals
    for offset in range(-2, 4):
        if "".join(list(map(str, winning_Sequence))) in "".join(list(map(str, np.flip(board, 1).diagonal(offset)))):
            return True

#Get all valid columns in the board
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

#Move to a random spot.  Each available spot has an equal likelihood of being chosen
def move_random(board, color):
    valid_locations = get_valid_locations(board)
    column = random.choice(valid_locations)
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)

#Move the agent, by simulating 100 random games for each column, and choosing the column based off of the column with the most wins
def MCagent(board, color):
  best_column = -1
  best_count = -1
  #For every column..
  for i in range(COLUMN_COUNT):
    #If column is not full...
    if is_valid_location(board, i):
        win_count = 0
        #Simulate 100 games, keeping track of which column does the best
        for j in range(100):
          win_count += play_game(np.copy(board), color, i)
        if win_count > best_count:
          best_count = win_count
          best_column = i
  row = get_next_open_row(board, best_column)
  drop_chip(board, row, best_column, RED_INT)
  return best_column

#Simulate a game for the agent.  If the column selected ultimately results in the agent winning, award 2 points.  1 for a tie and 0 for a loss
def play_game(board, RED_INT, col):
#First, move the agent to the selected column
  turn = 0
  game_over = False
  row = get_next_open_row(board, col)
  drop_chip(board, row, col, RED_INT)
  if game_is_won(board, RED_INT):
    return 2
    #Randomly play out the rest of the game
  while not game_over:
    #agent moving
      if turn % 2 == 0:
          move_random(board,RED_INT)
    #Nom-agent moving
      if turn % 2 == 1 and not game_over:
          move_random(board,BLUE_INT)

    #Award points
      if game_is_won(board, RED_INT):
          return 2
      if game_is_won(board, BLUE_INT):
          return 0
      if len(get_valid_locations(board)) == 0:
          return 1
      turn += 1


#Code for my heuristic agent is below, from hw3
def move_heuristic(board, color):
    score = -1000000
    column = -1
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            curr = board_score(board, col)
            if curr > score:
                score = curr
                column = col
    row = get_next_open_row(board, column)
    drop_chip(board, row, column, color)

def board_score(board, col):
    temp_board = board.copy()
    row = get_next_open_row(temp_board, col)
    temp_board[row][col] = 2

    if game_is_won(temp_board, 2):
        return 10000

    score = 0

    score += objective_position(col)
    score += offensive_score(temp_board)
    score -= defensive_score(temp_board)
    print('col: ' , col, " def: ",defensive_score(temp_board), ' off: ', offensive_score(temp_board), 'total: ', score)
    return score

def offensive_score(temp_board):
    score = 0

    sequence1 = '0222'
    sequence2 = '2022'
    sequence3 = '2202'
    sequence4 = '2220'
    threes = [sequence1, sequence2, sequence3, sequence4]

    sequence5 = '0022'
    sequence6 = '0202'
    sequence7 = '2002'
    sequence8 = '0220'
    sequence9 = '2020'
    sequence10 = '2200'
    twos = [sequence5, sequence6, sequence7, sequence8, sequence9, sequence10]

    # Add 10 points for 3 in a row horizontal, and 3 pts for 2 in a row
    for r in range(ROW_COUNT):
        for seq in threes:
            if seq in "".join(list(map(str, temp_board[r, :]))):
                score += 10
        for seq in twos:
            if seq in "".join(list(map(str, temp_board[r, :]))):
                score += 3

    # Add 8 points for 3 in a row vertical, and 2 pts for 2 in a row
    for c in range(COLUMN_COUNT):
        if sequence4 in "".join(list(map(str, temp_board[:, c]))):
            score += 8
        if sequence10 in "".join(list(map(str, temp_board[:, c]))):
            score += 2

    # Check positively sloped diagonals
    # Add 10 points for 3 in a row horizontal, and 3 pts for 2 in a row
    for offset in range(-2, 4):
        for seq in threes:
            if seq in "".join(list(map(str, temp_board.diagonal(offset)))):
                score += 10
        for seq in twos:
            if seq in "".join(list(map(str, temp_board.diagonal(offset)))):
                score += 3
    # Check negatively sloped diagonals
    # Add 10 points for 3 in a row horizontal, and 3 pts for 2 in a row
    for offset in range(-2, 4):
        for seq in threes:
            if seq in "".join(list(map(str, np.flip(temp_board, 1).diagonal(offset)))):
                score += 10
        for seq in twos:
            if seq in "".join(list(map(str, temp_board.diagonal(offset)))):
                score += 3
    return score


def defensive_score(temp_board):
    score = 0

    sequence1 = '0111'
    sequence2 = '1011'
    sequence3 = '1110'
    sequence4 = '1110'
    threes = [sequence1, sequence2, sequence3, sequence4]

    sequence5 = '0011'
    sequence6 = '0101'
    sequence7 = '1001'
    sequence8 = '0110'
    sequence9 = '1010'
    sequence10 = '1100'
    twos = [sequence5, sequence6, sequence7, sequence8, sequence9, sequence10]

    # Add 10 points for 3 in a row horizontal, and 3 pts for 2 in a row
    for r in range(ROW_COUNT):
        for seq in threes:
            if seq in "".join(list(map(str, temp_board[r, :]))):
                print('found')
                score += 100
        for seq in twos:
            if seq in "".join(list(map(str, temp_board[r, :]))):
                score += 4

    # Add 8 points for 3 in a row vertical, and 2 pts for 2 in a row
    for c in range(COLUMN_COUNT):
        if sequence4 in "".join(list(map(str, temp_board[:, c]))):
            score += 100
        if sequence10 in "".join(list(map(str, temp_board[:, c]))):
            score += 1

    # Check positively sloped diagonals
    # Add 10 points for 3 in a row horizontal, and 3 pts for 2 in a row
    for offset in range(-2, 4):
        for seq in threes:
            if seq in "".join(list(map(str, temp_board.diagonal(offset)))):
                score += 100
        for seq in twos:
            if seq in "".join(list(map(str, temp_board.diagonal(offset)))):
                score += 4
    # Check negatively sloped diagonals
    # Add 10 points for 3 in a row horizontal, and 3 pts for 2 in a row
    for offset in range(-2, 4):
        for seq in threes:
            if seq in "".join(list(map(str, np.flip(temp_board, 1).diagonal(offset)))):
                score += 100
        for seq in twos:
            if seq in "".join(list(map(str, temp_board.diagonal(offset)))):
                score += 4
    return score

def objective_position(col):
    if col == 1 or col == 5:
        return 1
    if col == 2 or col == 4:
        return 2
    if col == 3:
        return 3
    return 0



# # # # # # # # # # # # # # main execution of the game # # # # # # # # # # # # # #
turn = 0

board = create_board()
print_board(board)
game_over = False

while not game_over:
    #Agent's move
    if turn % 2 == 0:
        move_agent(board, RED_INT)

    #Non-agent's move, which can either be random or heuristic
    if turn % 2 == 1 and not game_over:
        move_heuristic(board, BLUE_INT)
        #move_random(board,BLUE_INT)

    print_board(board)
    
    if game_is_won(board, RED_INT):
        game_over = True
        print('Red wins!')
    if game_is_won(board, BLUE_INT):
        game_over = True
        print('Blue wins!')
    if len(get_valid_locations(board)) == 0:
        game_over = True
        print('Draw!')
    turn += 1