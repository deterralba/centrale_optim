#!/usr/bin/env python3

import numpy as np
from time import time

DEFAULT_VALUE = -1

# A = 10, B = 11, C = 12, D = 13, E = 14, F = 15
LINE_DOWN  = (4, 5, 6,  7,  12, 13, 14, 15)  # CDEF
LINE_UP    = (1, 3, 5,  7,  9,  11, 13, 15)  # BDF
LINE_LEFT  = (2, 3, 6,  7,  10, 11, 14, 15)  # ABEF
LINE_RIGHT = (8, 9, 10, 11, 12, 13, 14, 15)  # ABCDEF
LINES = {
    'up': LINE_UP,
    'down': LINE_DOWN,
    'left': LINE_LEFT,
    'right': LINE_RIGHT
}

ONE   = (1, 2, 4, 8)
THREE = (7, 11, 13, 14)  # BDE
FOUR  = (15, )
TWO_CORNER   = (5, 10)  # A
TWO_STRAIGHT = (3,  6, 9, 12)  # C
SHAPES_BY_SIZE = [ONE, TWO_CORNER, TWO_STRAIGHT, THREE, FOUR, (0,), (15,)]

class NoSolutionError(Exception):
    pass

def solve(original_problem, find_only_one=False, GUI_callback=(lambda problem, valid=False: None)):
    pile = []
    solutions = []
    try:
        solutions.append(find_solution(original_problem, pile, GUI_callback))
    except NoSolutionError:
        pass

    if find_only_one:
        return solutions.pop()
    else:
        while pile:
            try:
                solutions.append(
                    find_solution(original_problem, pile, GUI_callback, try_next_solution(pile))
                )
            except NoSolutionError:
                pass
    return solutions

def find_solution(original_problem, pile, GUI_callback, solution=None):
    nb_deadends = 0
    if solution is None:
        solution = np.zeros(original_problem.shape, dtype=np.int32) + DEFAULT_VALUE
    while not is_finished(solution):
        square = get_next_square(solution)
        choices = get_possible_choices(original_problem, solution, square)
        if choices:
            choice = choices.pop()
            solution[square] = choice
            GUI_callback(solution)
            if choices:
                pile = add_choices_to_pile(solution, pile, square, choices)
        else:
            nb_deadends += 1
            solution = try_next_solution(pile)
    GUI_callback(solution, valid=True)
    # print('number of deadends:', nb_deadends)
    return solution

def try_next_solution(pile):
    if pile:
        solution, square, choice = pile.pop()
        solution[square] = choice
        return solution
    else:
        raise NoSolutionError('no more entries in pile')

def add_choices_to_pile(solution, pile, square, choices):
    for choice in choices:
        pile.append((np.copy(solution), square, choice))
    return pile

def get_possible_choices(original_problem, solution, square):
    choices = []
    constrains = get_constrains(solution, square)
    for alternative in get_alternatives(original_problem[square]):
        if satisfy_constrains(alternative, constrains):
            choices.append(alternative)
    return choices

def get_alternatives(shape):
    for shapes in SHAPES_BY_SIZE:
        if shape in shapes:
            return shapes
    else:
        raise ValueError('unknown shape {}'.format(shape))

def satisfy_constrains(shape, constrains):
    # k takes the values up, left, down, right
    for k, cons in constrains.items():
        if cons is None:
            continue
        elif cons is False and shape in LINES[k]:
            return False
        elif cons is True and shape not in LINES[k]:
            return False
    return True

def get_constrains(solution, square):
    line, col = square
    nb_line = solution.shape[0] - 1
    nb_col  = solution.shape[1] - 1

    if line == 0:
        line_up = False
    else:
        up_square = solution[line - 1, col]
        if up_square == DEFAULT_VALUE:
            line_up = None
        elif up_square in LINE_DOWN:
            line_up = True
        else:
            line_up = False

    if line == nb_line:
        line_down = False
    else:
        down_square = solution[line + 1, col]
        if down_square == DEFAULT_VALUE:
            line_down = None
        elif down_square in LINE_UP:
            line_down = True
        else:
            line_down = False

    if col == 0:
        line_left = False
    else:
        left_square = solution[line, col - 1]
        if left_square == DEFAULT_VALUE:
            line_left = None
        elif left_square in LINE_RIGHT:
            line_left = True
        else:
            line_left = False

    if col == nb_col:
        line_right = False
    else:
        right_square = solution[line, col + 1]
        if right_square == DEFAULT_VALUE:
            line_right = None
        elif right_square in LINE_LEFT:
            line_right = True
        else:
            line_right = False

    lines = {
        'up': line_up,
        'down': line_down,
        'left': line_left,
        'right': line_right
    }
    # print('Constrains for {} {}: {}\nin {}'.format(line, col, lines, solution))
    return lines

def get_next_square(solution):
    for i in range(solution.shape[0]):
        for j in range(solution.shape[1]):
            if solution[i, j] == DEFAULT_VALUE:
                return (i, j)
    else:
        raise ValueError('no next square: {}'.format(solution))

def is_finished(solution):
    try:
        get_next_square(solution)
        return False
    except ValueError:
        return True


if __name__ == '__main__':

    import misc
    args = misc.read_args()

    EXAMPLE = args.example
    INPUT_PROBLEM = args.console_input
    GUI = not args.nogui
    GUI_FAST= args.fast
    GUI_SHOW_STEPS = args.show_steps

    if INPUT_PROBLEM:
        problem = np.array(misc.get_input(), dtype=np.int32)
    else:
        problem = misc.get_example(EXAMPLE)

    if GUI:
        from GUI import start_GUI
        start_GUI(problem, SHOW_STEPS=GUI_SHOW_STEPS, FAST=GUI_FAST)
    else:
        start = time()
        solutions = solve(problem)
        misc.console_print_solutions(solutions, start)
