#!/usr/bin/env python3

from copy import deepcopy
from itertools import permutations
from collections import defaultdict


def column(matrix, j):
    return [row[j] for row in matrix]

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
    n = len(clues) // 4
    ind_diff = 3 * n - 1
    if is_row:
        # for rows, we need to add n
        clue_lt_ind = n + ind_diff - row_or_col_num
        clue_rb_ind = n + row_or_col_num
    else:
        clue_lt_ind = row_or_col_num
        clue_rb_ind = ind_diff - row_or_col_num
    return clues[clue_lt_ind], clues[clue_rb_ind]

def possible_lines(n, clue_lt, clue_rb):
    # find what lines are possible given two clues
    perm = permutations([i for i in range(1, n+1)])
    possible = []
    for p in perm:
        if is_clue_satisfied(p, clue_lt, clue_rb):
            possible.append(list(p))
    return possible

def line_values(row_or_col_num, clues, is_row=True):
    # return a dictionary of index-value pairs
    n = len(clues) // 4
    clue_lt, clue_rb = get_clues(row_or_col_num, clues, is_row=is_row)
    possible = possible_lines(n, clue_lt, clue_rb)
    pos_vals = {}
    for j in range(n):
        vals = set(column(possible, j))
        index = (row_or_col_num, j)[::(2 * is_row) - 1]
        pos_vals[index] = vals
    return pos_vals

def possible_values(clues):
    n = len(clues) // 4
    row_clues = []
    col_clues = []
    row_vals = {}
    col_vals = {}
    #for i in range(n):
    #    row_clues.append(get_clues(i, clues, is_row=True))
    #    col_clues.append(get_clues(i, clues, is_row=False))
    for i in range(n):
        row_vals.update(line_values(i, clues, is_row=True))
        col_vals.update(line_values(i, clues, is_row=False))
    #all_vals = {(i, j): set(k for k in range(1, n+1)) for i in range(n) for j in
    #            range(n)}
    pos_vals = {}
    sort_list = lambda x: sorted(list(x))
    for i in range(n):
        for j in range(n):
            ij = (i, j)
            if ij in row_vals and ij in col_vals:
                vals = row_vals[ij] & col_vals[ij]
            elif ij in row_vals:
                vals = pos_vals[ij]
            else:
                vals = col_vals[ij]
            pos_vals[ij] = sort_list(vals)
    return pos_vals

def obvious_board(clues):
    n = len(clues) // 4
    board = [[0] * n for i in range(n)]
    pos_vals = possible_values(clues)
    for (i, j), v in pos_vals.items():
        if len(v) == 1:
            board[i][j] = v[0]
    return board

def next_empty(board):
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == 0:
                return (i, j)
    return False

def next_empty_smart(board, clues):
    pass

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
    n = len(clues) // 4
    row, col = coord
    if cand in board[row] or cand in column(board, col):
        return None
    is_valid_row = is_valid_col = True
    cand_board = deepcopy(board)
    cand_board[coord[0]][coord[1]] = cand
    if 0 in cand_board[row] and 0 in column(cand_board, col):
        return cand_board
    # TODO: col == 0 ?
    if col == n-1:
        # TODO: calculating clue every time
        clue_lt_rb = get_clues(row, clues, is_row=True)
        is_valid_row = is_clue_satisfied(cand_board[row], *clue_lt_rb)
    # TODO: row == 0 ?
    if row == n-1:
        clue_lt_rb = get_clues(col, clues, is_row=False)
        is_valid_col = is_clue_satisfied(column(cand_board, col), *clue_lt_rb)

    if is_valid_row and is_valid_col:
        return cand_board
    else:
        return None

def solve_puzzle(clues, board=None):
    n = len(clues) // 4
    if not board:
        #board = [[0] * n for i in range(n)]
        board = obvious_board(clues)
    coord = next_empty(board)
    if not coord:
        a = tuple(tuple(row) for row in board)
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
    clues4 = (
        ( 2, 2, 1, 3,
          2, 2, 3, 1,
          1, 2, 2, 3,
          3, 2, 1, 3 ),
        ( 0, 0, 1, 2,
          0, 2, 0, 0,
          0, 3, 0, 0,
          0, 1, 0, 0 )
    )
    outcomes4 = (
        ( ( 1, 3, 4, 2 ),
          ( 4, 2, 1, 3 ),
          ( 3, 4, 2, 1 ),
          ( 2, 1, 3, 4 ) ),
        ( ( 2, 1, 4, 3 ),
          ( 3, 4, 1, 2 ),
          ( 4, 2, 3, 1 ),
          ( 1, 3, 2, 4 ) )
    )
    #correct = [solve_puzzle(clues[i]) == outcomes[i] for i in
    #           range(len(clues))]
    #print(correct)

    clues6 = (
        ( 3, 2, 2, 3, 2, 1,
          1, 2, 3, 3, 2, 2,
          5, 1, 2, 2, 4, 3,
          3, 2, 1, 2, 2, 4 )
    )
    outcomes6 = (
        ( ( 2, 1, 4, 3, 5, 6 ),
          ( 1, 6, 3, 2, 4, 5 ),
          ( 4, 3, 6, 5, 1, 2 ),
          ( 6, 5, 2, 1, 3, 4 ),
          ( 5, 4, 1, 6, 2, 3 ),
          ( 3, 2, 5, 4, 6, 1 ) )
    )

    correct = solve_puzzle(clues6) == outcomes6
    print(correct)

    #print(obvious_board(clues6))
    #print(line_values(0, clues4[0], is_row=False))


