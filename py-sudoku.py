import random
import numpy as np


def read_puzzle(in_line):
    """
    reads a sudoku puzzle from a single input line
    :param in_line: 9 space-separated 9-digit numbers ranging from 0-9
    :return: returns the numbers in a numpy array
    """
    arr = np.zeros((9,9), dtype=int)
    for i, line in enumerate(in_line.split(' ')):
        for j, num in enumerate(list(line)):
            arr[i, j] = num

    return arr


def test_fit(x, y, n, board_state):
    """
    tests whether n can be placed in x,y on the current board_state
    :param x: horizontal position on the board
    :param y: vertical position on the board
    :param n: the number to place
    :param board_state: the current board state as a numpy array
    :return: true if nothing would stop n from being placed in x,y on board_state, else returns false
    """

    # first test if something is already in that position
    if board_state[x, y] != 0:
        return False

    # then test if n already exists in that column or row
    for i in range(9):
        if board_state[x, i] == n:
            return False
        elif board_state[i, y] == n:
            return False

    # finally test if it fits in the block
    x_block = 0
    y_block = 0

    if x < 3:
        x_block = 0
    elif x < 6:
        x_block = 1
    else:
        x_block = 2

    if y < 3:
        y_block = 0
    elif y < 6:
        y_block = 1
    else:
        y_block = 2

    for i in range(x_block * 3, x_block * 3 + 3):
        for j in range(y_block * 3, y_block * 3 + 3):
            if board_state[i, j] == n:
                return False

    return True


def generate_puzzle(difficulty='easy'):
    """
    creates a sudoku puzzle
    :param difficulty: easy, medium, hard, impossible accepted
    :return: a 9x9 numpy array of valid sudoku
    """

    num_clues = 0

    # define a random-ish amount of clues based on the difficulty
    if difficulty == 'easy':
        for i in range(9):
            num_clues += random.randint(3,5)
    elif difficulty == 'medium':
        for i in range(9):
            num_clues += random.randint(2,4)
    elif difficulty == 'hard':
        for i in range(9):
            num_clues += random.randint(1,3)
    elif difficulty == 'impossible':
        for i in range(9):
            num_clues += random.randint(0,2)

    # create the playboard, or puzzle
    playboard = np.zeros((9,9), dtype=int)

    # always make sure a number can be placed on the board
    while num_clues > 0:
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        n = random.randint(1, 9)

        if test_fit(x, y, n, playboard):
            playboard[x, y] = n
            num_clues -= 1

    return playboard


def narrow_solutions(x, y, board_state):
    """
    tests all numbers 1-9 whether they could fit in spot x,y on the current board
    :param x: horizontal position
    :param y: vertical position
    :param board_state: current board as a 9x9 valid sudoku puzzle
    :return: returns a numpy array of bools indicating whether that index(+1) would fit in x,y
    """
    solutions = np.array([True, True, True, True, True, True, True, True, True])

    for i in range(1, 10):  # numbers from 1 to 9
        # test for vertical and horizontal
        for j in range(9):
            if board_state[x, j] == i:
                solutions[i - 1] = False
                break
            elif board_state[j, y] == i:
                solutions[i - 1] = False
                break

        # finally test if it exists in the block
        x_block = 0
        y_block = 0

        if x < 3:
            x_block = 0
        elif x < 6:
            x_block = 1
        else:
            x_block = 2

        if y < 3:
            y_block = 0
        elif y < 6:
            y_block = 1
        else:
            y_block = 2

        for j in range(x_block * 3, x_block * 3 + 3):
            for k in range(y_block * 3, y_block * 3 + 3):
                if board_state[j, k] == i:
                    solutions[i - 1] = False

    return solutions


def catch_error(list_like):
    """
    if none of the options are true, something has gone wrong
    :param list_like: a list_like of bools
    :return: true if at least one is true, else returns false
    """
    for b in list_like:
        if b:
            return True

    return False


def single_option(list_like):
    """
    checks if a single option is true
    :param list_like: a list-like of bools
    :return: true if exactly 1 is true, else returns false
    """
    trues = 0
    num = 0
    for i, b in enumerate(list_like):
        if b:
            trues += 1
            num = i + 1
            if trues > 1:
                return 0
    return num


def iterate_through_block(n, x, y, state, solution_state):
    """
    goes through a 3x3 block to check for n
    :param n:
    :param x:
    :param y:
    :param state:
    :param solution_state:
    :return:
    """
    num_n = 0
    pos = (0, 0)

    # go though each position in the block looking for n
    for i in range(x * 3, x * 3 + 3):
        for j in range(y * 3, y * 3 + 3):
            if state[i, j] == n + 1:
                return 0, (0, 0)  # break all the way out of the block because the number already exists here

            if state[i, j] != 0:  # make sure nothing is here already
                continue

            # this position is valid, check if it can be n
            if solution_state[i, j, n]:
                num_n += 1
                pos = (i, j)

    return num_n, pos


def check_area(current_state, current_solution_state):
    # first check for rows where only one box can have a number (n)
    for n in range(9):  # current number we are working with (to access in current_solution_state)
        for i in range(9):  # current row we are in
            num_n = 0
            pos = (0, 0)
            for j in range(9):  # current index in the row
                if current_state[i, j] == n + 1:
                    break  # break all the way out of the row because the number already exists here

                if current_state[i, j] != 0:  # make sure nothing is here already
                    continue

                # this position is valid, check if it can be n
                if current_solution_state[i, j, n]:
                    num_n += 1
                    pos = (i, j)

            # now we are done with that row, so check if there was one single solution
            if num_n == 1:
                current_state[pos[0], pos[1]] = n + 1  # if one solution existed, the state is updated and we return
                return current_state

    # then do the same with columns
    for n in range(9):  # current number we are working with (to access in current_solution_state)
        for i in range(9):  # current column we are in
            num_n = 0
            pos = (0, 0)
            for j in range(9):  # current index in the row
                if current_state[j, i] == n + 1:
                    break  # break all the way out of the row because the number already exists here

                if current_state[j, i] != 0:  # make sure nothing is here already
                    continue

                # this position is valid, check if it can be n
                if current_solution_state[j, i, n]:
                    num_n += 1
                    pos = (j, i)

            # now we are done with that row, so check if there was one single solution
            if num_n == 1:
                current_state[pos[0], pos[1]] = n + 1  # if one solution existed, the state is updated and we return
                return current_state

    # finally, check the blocks
    # this can be done by just iterating through them
    for n in range(9):  # the number we are looking for
        for x in range(3):  # the horizontal block from 0 to 2
            for y in range(3):  # the vertical block from 0 to 2
                num_n, pos = iterate_through_block(n, x, y, current_state, current_solution_state)
                if num_n == 1:  # there was exactly one square that could be n
                    current_state[pos[0], pos[1]] = n + 1
                    return current_state

    return current_state  # that was a fluke (but it should have worked)


def sudoku_is_complete(state):
    for i in range(9):
        for j in range(9):
            if(state[i,j] == 0):
                return False

    return True


def solver(puzzle_input):
    puzzle_is_solved = False

    # create a board of possible solutions of each unsolved square
    solutions_board = np.zeros((9,9,9))
    for i in range(9):
        for j in range(9):
            if puzzle_input[i, j] == 0:
                solutions_board[i, j] = np.array([True, True, True, True, True, True, True, True, True])

    num_iterations = 0
    # iterate through these until the puzzle is solved
    while not puzzle_is_solved:
        did_something = False

        for i in range(9):
            for j in range(9):
                if puzzle_input[i, j] != 0:
                    continue
                # first, narrow down options in that spot based on row, column and block
                solutions_board[i, j] = narrow_solutions(i, j, puzzle_input)

                # check for errors first
                if not catch_error(solutions_board[i, j]):
                    print("There was an unsolvable error at", i, j)
                    puzzle_input[i, j] = 69
                    return puzzle_input

                # now check if this position only has one option
                single_solution = single_option(solutions_board[i, j])
                if single_solution > 0:
                    puzzle_input[i, j] = single_solution
                    did_something = True

        if not did_something:   # only check areas if nothing happened last iteration since it is unnecessary,
                                # resource intensive, and might break something by using outdated possibilities
            puzzle_input = check_area(puzzle, solutions_board)

        num_iterations += 1

        if sudoku_is_complete(puzzle_input):
            print("Sudoku complete")
            break

        if num_iterations > 1000:
            print("Something might be wrong here, aborting")
            return puzzle_input

    return puzzle_input


# puzzle = generate_puzzle()

puzzle = read_puzzle(input("Please input a string equating a sudoku board: "
                           "\n9 space-separated 9-long series of numbers from 0-9 where 0 indicates empty"
                           "\n"))

print(puzzle)

solved = solver(puzzle)
print(solved)
