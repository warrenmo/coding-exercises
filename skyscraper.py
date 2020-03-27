#!/usr/bin/env python3

from copy import deepcopy
from itertools import permutations
from collections import defaultdict


class Skyscraper(object):
    def __init__(self, clues, obvious=True):
        self.clues = clues
        self.obvious = obvious

        self.n = len(clues) // 4
        self.board = self.starting_board()
        self.num_guesses = 0
        #print(self.board)

    @staticmethod
    def column(matrix, j):
        return [row[j] for row in matrix]

    def get_clues(self, row_or_col_num, is_row=True):
        # first, assume the board is square
        # next, we know that each line of skyscrapers has at most two clues 
        # but we need to index into the 'clues' input to access them
        # we observe that the difference between the two indices (one for each
        # clue) is (3n - 1 - 2 * row_or_col_num) where n is the side length of
        # the board
        #           0   1   2   3
        #   
        #   15      x   x   x   x       4
        #   14      x   x   x   x       5
        #   13      x   x   x   x       6
        #   12      x   x   x   x       7
        #
        #           11  10  9   8
        #
        #           0   1   2   3   4   5
        #   
        #   23      x   x   x   x   x   x   6
        #   22      x   x   x   x   x   x   7
        #   21      x   x   x   x   x   x   8
        #   20      x   x   x   x   x   x   9 
        #   19      x   x   x   x   x   x   10
        #   18      x   x   x   x   x   x   11
        #
        #           17  16  15  14  13  12
        #n = len(clues) // 4
        ind_diff = 3 * self.n - 1
        if is_row:
            # for rows, we need to add n
            clue_lt_ind = self.n + ind_diff - row_or_col_num
            clue_rb_ind = self.n + row_or_col_num
        else:
            clue_lt_ind = row_or_col_num
            clue_rb_ind = ind_diff - row_or_col_num
        return self.clues[clue_lt_ind], self.clues[clue_rb_ind]

    @staticmethod
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
        return clue_lt_ == seen_lt and clue_rb_ == seen_rb
        #if clue_lt_ == seen_lt and clue_rb_ == seen_rb:
        #    return True
        #else:
        #    return False

    def possible_lines(self, clue_lt, clue_rb):
        # find what lines are possible given two clues
        perm = permutations([i for i in range(1, self.n+1)])
        possible = []
        num_lines = 0
        for p in perm:
            if self.is_clue_satisfied(p, clue_lt, clue_rb):
                possible.append(list(p))
                num_lines += 1
        return possible, num_lines

    def line_values(self, row_or_col_num, is_row=True):
        # return a dictionary of index-value pairs
        clue_lt, clue_rb = self.get_clues(row_or_col_num, is_row=is_row)
        possible, num_lines = self.possible_lines(clue_lt, clue_rb)
        pos_vals = {}
        for j in range(self.n):
            vals = set(self.column(possible, j))
            index = (row_or_col_num, j)[::(2 * is_row) - 1]
            pos_vals[index] = vals
        return pos_vals, num_lines

    def possible_values(self):
        row_clues = []
        col_clues = []
        row_vals = {}
        col_vals = {}
        num_vals = {}
        #col_num_vals = {}
        for i in range(self.n):
            rv, r_num = self.line_values(i, is_row=True)
            cv, c_num = self.line_values(i, is_row=False)
            row_vals.update(rv)
            col_vals.update(cv)
            num_vals['row-' + str(i)] = r_num
            num_vals['col-' + str(i)] = c_num
            #col_num_vals[i] = c_num
        #all_vals = {(i, j): set(k for k in range(1, n+1)) for i in range(n) for j in
        #            range(n)}
        pos_vals = {}
        sort_list = lambda x: sorted(list(x))
        for i in range(self.n):
            for j in range(self.n):
                ij = (i, j)
                if ij in row_vals and ij in col_vals:
                    vals = row_vals[ij] & col_vals[ij]
                elif ij in row_vals:
                    vals = pos_vals[ij]
                else:
                    vals = col_vals[ij]
                pos_vals[ij] = sort_list(vals)
        return pos_vals, num_vals

    def update_possible_values(self, index, value, pos_vals):
        i, j = index
        #print(pos_vals)
        pos_vals_ = deepcopy(pos_vals)
        for k in range(self.n):
            if value in pos_vals_[(i, k)]:
                pos_vals_[(i, k)].remove(value)
            if value in pos_vals_[(k, j)]:
                pos_vals_[(k, j)].remove(value)
        pos_vals_[index] = [value]
        return pos_vals_

    def starting_board(self):
        board = [[0] * self.n for i in range(self.n)]
        if self.obvious:
            pos_vals, _ = self.possible_values()
            for (i, j), v in pos_vals.items():
                if len(v) == 1:
                    board[i][j] = v[0]
        return board

    # TODO: reconcile output types with smart_cell_order
    def next_empty(self):
        for i, row in enumerate(self.board):
            for j, val in enumerate(row):
                if val == 0:
                    return (i, j)
        return False

    # TODO: reconcile output types with next_empty
    def smart_cell_order(self):
        if 0 not in [x for row in self.board for x in row]:
            return [], {}
        bins = defaultdict(list)
        pos_vals, num_vals = self.possible_values()
        line_order = [k for k, _ in sorted(num_vals.items(), key=lambda x: x[1])]
        already_counted = set()
        order = []
        for line in line_order:
            row_or_col, num = line.split('-')
            num = int(num)
            if row_or_col == 'row':
                ind = 0
            else:
                ind = 1
            line_pos_vals = {k: v for k, v in pos_vals.items() if k[ind] == num}
            line_ord = [k for k, _ in sorted(line_pos_vals.items(), key=lambda x: len(x[1]))
                        if k[ind] == num and k not in already_counted]
            already_counted |= set(line_ord)
            order += line_ord
        # TODO: shouldn't have to do this
        if self.obvious:
            order = list(filter(lambda x: len(pos_vals[x]) > 1, order))
        return order, pos_vals

    def smart_cell_order_old(self):
        bins = defaultdict(list)
        pos_vals, _ = self.possible_values()
        #print(pos_vals)
        for k, v in pos_vals.items():
            if self.board[k[0]][k[1]] == 0:
                num_vals = len(v)
                if self.obvious:
                    if num_vals > 1:
                        bins[num_vals].append(k)
                else:
                    bins[num_vals].append(k)
        return [v for k in sorted(bins.keys()) for v in bins[k]]

    def is_valid(self, cand, coord):
        row, col = coord
        if cand in self.board[row] or cand in self.column(self.board, col):
            return None
        is_valid_row = is_valid_col = True
        cand_board = deepcopy(self.board)
        cand_board[coord[0]][coord[1]] = cand
        is_row_full = is_col_full = False
        if 0 in cand_board[row] and 0 in self.column(cand_board, col):
            return cand_board
        if 0 not in cand_board[row]:
            #print(cand_board[row])
            is_row_full = True
        if 0 not in self.column(cand_board, col):
            #print(column(cand_board, col))
            is_col_full = True
        if is_row_full:
            # TODO: calculating clue every time
            clue_lt_rb = self.get_clues(row, is_row=True)
            is_valid_row = self.is_clue_satisfied(cand_board[row], *clue_lt_rb)
        if is_col_full:
            clue_lt_rb = self.get_clues(col, is_row=False)
            is_valid_col = self.is_clue_satisfied(self.column(cand_board, col), *clue_lt_rb)

        if is_valid_row and is_valid_col:
            #if is_row_full:
            #    print('Row: {}'.format(row))
            #    print(cand_board)
            #    print(clue_lt_rb)
            #    print()
            #elif is_col_full:
            #    print('Col: {}'.format(col))
            #    print(cand_board)
            #    print(clue_lt_rb)
            #    print()
            self.board = cand_board
            return cand_board
        else:
            return None

    def solve(self):
        #print('hi')
        coord = self.next_empty()
        if not coord:
            a = tuple(tuple(row) for row in self.board)
            return a
        else:
            for cand in range(1, self.n+1):
                self.num_guesses += 1
                old_board = self.board
                cand_board = self.is_valid(cand, coord)
                #print(cand, coord)
                if cand_board is not None:
                    #print(cand_board)
                    self.board = cand_board
                    next_board = self.solve()#board=cand_board)
                    if next_board:
                        return next_board
                    else:
                        self.board = old_board
                        continue
                else:
                    continue
            return False

    def solve_smart(self, cell_order=[], value_options={}):
        print('hi')
        if cell_order == []:
            # TODO: calls this when board is complete
            # TODO: repeats obvious calculations
            cell_order, value_options = self.smart_cell_order()
            #print(cell_order)
            #print(len(cell_order))
            #print(board)
        if cell_order == []:
            a = tuple(tuple(row) for row in self.board)
            return a
        else:
            #print(cell_order)
            coord = cell_order[0]
            for cand in value_options[coord]:
                self.num_guesses += 1
                old_board = self.board
                cand_board = self.is_valid(cand, coord)
                if cand_board is not None:
                    #print(cand_board)
                    self.board = cand_board
                    value_options_ = self.update_possible_values(coord, cand, value_options)
                    next_board = self.solve_smart(cell_order=cell_order[1:],
                                                  value_options=value_options_)
                    if next_board:
                        return next_board
                    else:
                        self.board = old_board
                        continue
                else:
                    continue
            return False

def solve_puzzle(clues, obvious=True):
    skyscraper = Skyscraper(clues, obvious=obvious)
    solution = skyscraper.solve()
    num_guesses = skyscraper.num_guesses
    return solution, num_guesses

def solve_puzzle_smart(clues, obvious=True):
    skyscraper = Skyscraper(clues, obvious=obvious)
    solution = skyscraper.solve_smart()
    num_guesses = skyscraper.num_guesses
    return solution, num_guesses


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
          3, 2, 1, 2, 2, 4 ),
        ( 0, 0, 0, 2, 2, 0,
          0, 0, 0, 6, 3, 0,
          0, 4, 0, 0, 0, 0,
          4, 4, 0, 3, 0, 0 ),
        ( 0, 3, 0, 5, 3, 4,
          0, 0, 0, 0, 0, 1,
          0, 3, 0, 3, 2, 3,
          3, 2, 0, 3, 1, 0 )
    )
    outcomes6 = (
        ( ( 2, 1, 4, 3, 5, 6 ),
          ( 1, 6, 3, 2, 4, 5 ),
          ( 4, 3, 6, 5, 1, 2 ),
          ( 6, 5, 2, 1, 3, 4 ),
          ( 5, 4, 1, 6, 2, 3 ),
          ( 3, 2, 5, 4, 6, 1 ) ),
        ( ( 5, 6, 1, 4, 3, 2 ),
          ( 4, 1, 3, 2, 6, 5 ),
          ( 2, 3, 6, 1, 5, 4 ),
          ( 6, 5, 4, 3, 2, 1 ),
          ( 1, 2, 5, 6, 4, 3 ),
          ( 3, 4, 2, 5, 1, 6 ) ),
        ( ( 5, 2, 6, 1, 4, 3 ),
          ( 6, 4, 3, 2, 5, 1 ),
          ( 3, 1, 5, 4, 6, 2 ),
          ( 2, 6, 1, 5, 3, 4 ),
          ( 4, 3, 2, 6, 1, 5 ),
          ( 1, 5, 4, 3, 2, 6 ) )
    )

    obvious = True

    #s,n = solve_puzzle(clues4[0], obvious=obvious)
    #correct = s == outcomes4[0]
    #s,n = solve_puzzle(clues4[1], obvious=obvious)
    #correct = s == outcomes4[1]
    #s,n = solve_puzzle(clues6[0], obvious=obvious)
    #correct = s == outcomes6[0]
    #s,n = solve_puzzle(clues6[1], obvious=obvious)
    #correct = s == outcomes6[1]
    #s,n = solve_puzzle(clues6[2], obvious=obvious)
    #correct = s == outcomes6[2]

    #s,n = solve_puzzle_smart(clues4[0], obvious=obvious)
    #correct = s == outcomes4[0]
    #s,n = solve_puzzle_smart(clues4[1], obvious=obvious)
    #correct = s == outcomes4[1]
    #s,n = solve_puzzle_smart(clues6[0], obvious=obvious)
    #correct = s == outcomes6[0]
    #s,n = solve_puzzle_smart(clues6[1], obvious=obvious)
    #correct = s == outcomes6[1]
    s,n = solve_puzzle_smart(clues6[2], obvious=obvious)
    correct = s == outcomes6[2]

    print(correct)
    print(n)

