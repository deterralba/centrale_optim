def console_print_solutions(solutions, start):
    '''Prints on the console the solutions and the time ellapsed since start'''
    from time import time
    print('#'*60, '\n')
    if solutions:
        print('{} solution{} found:\n\n{}'.format(
            len(solutions),
            (' was' if len(solutions) == 1 else 's were'),
            '\n and \n'.join(str(s) for s in solutions))
        )
    else:
        print('This problem has no solution\n')
    print('\nSolving took {:.4f}s\n'.format(time()-start))
    print('#'*60)

def get_input():
    '''Asks the user to type a custom grid (must be a square). Try again if input is wrong'''
    try:
        return _ask_input()
    except Exception as e:
        print('\nPlease try again, you made an error: {}\n'.format(e))
        get_input()

def _ask_input():
    print('Please enter the first line of the problem')
    partial_problem = []
    partial_problem.append(input('> '))
    for i in range(len(partial_problem[0]) - 1):
        partial_problem.append(input('> '))

    clean_problem = []
    for line in partial_problem:
        for c in [('A', '10'), ('B', '11'), ('C', '12'), ('D', '13'), ('E', '14'), ('F', '15')]:
            line = line.replace(*c)
        clean_problem.append([int(shape) for shape in line])

    for l in clean_problem:
        for c in l:
            if not 0 <= c <= 15:
                raise ValueError('Values should be  between 0..9 and A..F')
    return clean_problem

def get_example(id):
    import numpy as np
    problem0 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]], dtype=np.int32)
    problem1 = np.array([[1, 7, 3],
                         [1, 3, 3],
                         [3, 5, 1]],
                        dtype=np.int32)
    problem2 = np.array([[1, 1, 1, 3, 3],
                         [7, 3, 3, 3, 5],
                         [3, 3, 3, 5, 3],
                         [3, 7, 5, 3, 1],
                         [3, 7, 5, 7, 3]],
                        dtype=np.int32)
    problem3 = np.array([[1, 0, 0, 0, 1],
                         [7, 3, 0, 3, 7],
                         [3, 3, 0, 3, 3],
                         [1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1]],
                        dtype=np.int32)
    problem4 = np.array([[3, 5, 5, 3, 3, 3, 1],
                         [3, 5, 5, 3, 3, 7, 1],
                         [1, 1, 3, 7, 3, 7, 3],
                         [1, 1, 3, 3, 3, 7, 3],
                         [1, 1, 3, 7, 3, 3, 1],
                         [3, 3, 3, 3, 1, 3, 1],
                         [0, 1, 3, 3, 1, 0, 1],
                         [1, 5, 5, 5, 3, 7, 3],
                         [3, 3, 3, 3, 0, 1, 0]],
                        dtype=np.int32).transpose()
    problems = [
        problem0,
        problem1,
        problem2,
        problem3,
        problem4,
    ]
    return problems[id]

def read_args():
    args = None
    import argparse
    import sys
    parser = argparse.ArgumentParser()

    # GUI
    parser.add_argument('-n', '--nogui',
                        help='Doesn\'t start the GUI',
                        action='store_true', default=False)
    parser.add_argument('-f', '--fast',
                        help='GUI: Hide all the alrgorithm steps.',
                        action='store_true', default=False)
    parser.add_argument('-p', '--show-steps',
                        help='GUI: Show all the arlgorithm steps.',
                        action='store_true', default=False)

    # INPUT
    parser.add_argument('-s', '--console-input',
                        help='Solve the problem given in the standard input',
                        action='store_true', default=False)
    parser.add_argument('-e', '--example',
                        help='Solve a known example, type a number between 0 and 4',
                        default='4', type=int)

    # SOLVER
    parser.add_argument('-c', '--forward-check',
                        help='Solve the problem with forward check',
                        action='store_true', default=False)
    parser.add_argument('-a', '--arc-consistency',
                        help='Solve the problem maintaining arc consistency (this set forward-check to True)',
                        action='store_true', default=False)

    args = parser.parse_args()
    return args
