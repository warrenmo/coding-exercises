#!/usr/bin/env python3

from copy import deepcopy
from collections import defaultdict

def next_empty(board):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                return (i, j)
    return False

def column(board, j):
    return [row[j] for row in board]

def get_clues(row_or_col_num, clues, is_row=True):
    # first, assume the board is square
    # next, we know that each line of skyscrapers has at most two clues 
    # but we need to index into the 'clues' input to access them
    # we observe that the difference between the two indices (one for each
    # clue) is (3n - 1 - 2 * row_or_col_num) where n is the side length of the
    # board
    #           0   1   2   3
    #   
    #   15      x   x   x   x       4
    #   14      x   x   x   x       5
    #   13      x   x   x   x       6
    #   12      x   x   x   x       7
    #
    #           11  10  9   8
    n = int(len(clues) ** (1/2))
    ind_diff = 3 * n - 1
    if is_row:
        # for rows, we need to add n
        clue_lt = n + ind_diff - row_or_col_num
        clue_rb = n + row_or_col_num
    else:
        clue_lt = row_or_col_num
        clue_rb = ind_diff - row_or_col_num
    return clues[clue_lt], clues[clue_rb]

def is_clue_satisfied(line, clue_lt, clue_rb):
    seen_lt = seen_rb = 0
    max_lt = max_rb = float('-inf')
    n = len(line)
    for i in range(n):
        if line[i] > max_lt:
            seen_lt += 1
            max_lt = line[i]
        if line[n-i-1] > max_rb:
            seen_rb += 1
            max_rb = line[n-i-1]
    exists_clue = lambda x, y: x if x != 0 else y
    clue_lt_ = exists_clue(clue_lt, seen_lt)
    clue_rb_ = exists_clue(clue_rb, seen_rb)
    if clue_lt_ == seen_lt and clue_rb_ == seen_rb:
        return True
    else:
        return False

def is_valid(cand, coord, board, clues):
    row, col = coord
    if cand in board[row] or cand in column(board, col):
        return None
    is_valid_row = is_valid_col = True
    cand_board = deepcopy(board)
    cand_board[coord[0]][coord[1]] = cand
    if 0 in cand_board[row] and 0 in column(cand_board, col):
        return cand_board
    # TODO: col == 0 ?
    if col == 3:
        # TODO: calculating clue every time
        clue_lt_rb = get_clues(row, clues, is_row=True)
        is_valid_row = is_clue_satisfied(cand_board[row], *clue_lt_rb)
    # TODO: row == 0 ?
    if row == 3:
        clue_lt_rb = get_clues(col, clues, is_row=False)
        is_valid_col = is_clue_satisfied(column(cand_board, col), *clue_lt_rb)

    if is_valid_row and is_valid_col:
        return cand_board
    else:
        return None

def solve_puzzle(clues, board=None):
    n = int(len(clues) ** (1/2))
    if not board:
        board = [[0] * n for i in range(n)]
    coord = next_empty(board)
    if not coord:
        a = tuple(tuple(row) for row in board)
        print(a)
        return a
    else:
        for cand in range(1, n+1):
            cand_board = is_valid(cand, coord, board, clues)
            if cand_board is not None:
                next_board = solve_puzzle(clues, board=cand_board)
                if next_board:
                    return next_board
                else:
                    continue
            else:
                continue
        return False


if __name__ == "__main__":
    clues = (
        ( 2, 2, 1, 3,
          2, 2, 3, 1,
          1, 2, 2, 3,
          3, 2, 1, 3 ),
        ( 0, 0, 1, 2,
          0, 2, 0, 0,
          0, 3, 0, 0,
          0, 1, 0, 0 )
    )
    outcomes = (
        ( ( 1, 3, 4, 2 ),
          ( 4, 2, 1, 3 ),
          ( 3, 4, 2, 1 ),
          ( 2, 1, 3, 4 ) ),
        ( ( 2, 1, 4, 3 ),
          ( 3, 4, 1, 2 ),
          ( 4, 2, 3, 1 ),
          ( 1, 3, 2, 4 ) )
    )
    correct = [solve_puzzle(clues[i]) == outcomes[i] for i in
               range(len(clues))]

