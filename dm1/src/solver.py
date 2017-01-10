#!/usr/bin/env python3

import numpy as np
from time import time
from copy import deepcopy

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

FORWARD_CHECK = True
ARC_CONSISTENCY = True

class NoSolutionError(Exception):
    pass

def solve(original_problem, find_only_one=False, GUI_callback=(lambda problem, valid=False: None)):
    empty_problem = np.zeros(original_problem.shape, dtype=np.int32) + DEFAULT_VALUE
    domains = get_domains(original_problem)
    pile = [(empty_problem, domains)]
    solutions = []
    while pile:
        try:
            solutions.append(
                find_solution(original_problem, pile, GUI_callback)
            )
            if solutions and find_only_one:
                return solutions.pop()
        except NoSolutionError:
            pass
    return solutions

def find_solution(original_problem, pile, GUI_callback):
    '''
        Returns a solution, by trying to complete the problems given in the pile.
        Raises NoSolutionError if there is no solution
    '''
    solution, domains = try_next_solution(pile)
    is_deadend = False
    nb_deadends = 0
    while not is_finished(solution, domains):
        square = get_next_square(solution, domains)

        # domain = get_domain_of_square(domains, square)
        # valid_domain = get_valid_domain(solution, square, domain)  # all shapes compatible with the 4 adjacent borders
        # domains = update_domains(domains, square, valid_domain)  # pure, update domains to remove the shapes not compatible

        domains, valid_domain, old_domain = update_square_domain(solution, domains, square)

        print('after update', square, valid_domain)
        #import pprint
        #pprint.pprint(domains)

        if not valid_domain:
            is_deadend = True
        else:
            choice = min(valid_domain)
            solution[square] = choice
            GUI_callback(solution)  # this has only on visual effect, it doesn't change the solution

            other_choices = valid_domain - {choice}
            if other_choices:
                pile = add_choices_to_pile(solution, domains, pile, square, valid_domain - {choice})

            if FORWARD_CHECK:
                domains, is_deadend = forward_check(solution, domains, square, old_domain, valid_domain)
                if ARC_CONSISTENCY:
                    pass

        if is_deadend:
            print('DEAD')
            nb_deadends += 1
            solution, domains = try_next_solution(pile)
            is_deadend = False
    GUI_callback(solution, valid=True)  # this has only on visual effect, it doesn't change the solution
    print('number of deadends:', nb_deadends)
    return solution

def forward_check(solution, domains, original_square, original_domain, original_valid_domain):
    if original_domain == original_valid_domain:  # the domain did not change
        return domains, False
    else:
        squares = get_adjacent_squares(solution, original_square)
        for square in squares:
            #old_domain = get_domain_of_square(domains, square)
            #valid_domain = get_valid_domain(solution, square, old_domain)  # all shapes compatible with the 4 adjacent borders
            #new_domains = update_domains(domains, square, valid_domain)  # pure, update domains to remove the shapes not compatible

            domains, valid_domain, old_domain = update_square_domain(solution, domains, square)
            print('FORWARD CHECK: removed {} from square {} (adjacent of {})'.format(old_domain - valid_domain, square, original_square))
            if not valid_domain:
                print('FORWARD CHECK detected a dead end !')
                return domains, True
        else:
            return domains, False

def update_square_domain(solution, domains, square):
    old_domain = get_domain_of_square(domains, square)
    valid_domain = get_valid_domain(solution, square, old_domain)  # all shapes compatible with the 4 adjacent borders
    new_domains = update_domains(domains, square, valid_domain)  # pure, update domains to remove the shapes not compatible
    return new_domains, valid_domain, old_domain

def get_adjacent_squares(solution, square):
    line, col = solution.shape
    l, c = square
    squares = set()
    if l >= 1:
        squares.add((l-1, c))
    if l <= line - 2:
        squares.add((l+1, c))
    if c >= 1:
        squares.add((l, c-1))
    if c <= col - 2:
        squares.add((l, c+1))
    return squares

def try_next_solution(pile):
    if pile:
        return pile.pop()
    else:
        raise NoSolutionError('no more entries in pile')

def add_choices_to_pile(solution, domains,  pile, square, domain):
    for choice in domain:
        new_solution = np.copy(solution)
        new_solution[square] = choice
        pile.append((new_solution, deepcopy(domains)))  # check that the deepcopy works, and use the restricted domains
    return pile

def update_domains(domains, square, valid_domain):  # impure
    new_domains = domains.copy()
    new_domains[square[0]][square[1]] = valid_domain
    return new_domains

def get_domain_of_square(domains, square):
    return domains[square[0]][square[1]]

def get_valid_domain(solution, square, domain):
    valid_domain = set()
    constrains = get_constrains(solution, square)
    for alternative in domain:
        if satisfy_constrains(alternative, constrains):
            valid_domain.add(alternative)
    return valid_domain

def get_domains(original_problem):  # tested, don't forget to update the test
    line, col =  original_problem.shape
    return [[set(get_alternatives(original_problem[l, c])) for c in range(col)] for l in range(line)]

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

def get_next_square(solution, domains):
    ''' Returns the position of the square with the smallest domain '''
    free_squares = _extract_free_squares_and_their_domain_size(solution, domains)
    mini = min(free_squares, key=lambda x: x[1])[0]
    return mini

def _extract_free_squares_and_their_domain_size(solution, domains):
    line, col = solution.shape
    free_squares = []
    for l in range(line):
        for c in range(col):
            if solution[l, c] == DEFAULT_VALUE:
                free_squares.append(((l, c), len(domains[l][c])))
    return free_squares

def is_finished(solution, domains):
    try:
        get_next_square(solution, domains)
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
