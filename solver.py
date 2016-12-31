import numpy as np
import time

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

def solve(original_problem, find_all=False, GUI_callback=lambda problem, valid=False: None):
    start = time.time()
    pile = []
    solutions = []
    solutions.append(
        find_solution(original_problem, pile, GUI_callback)
    )
    if find_all:
        while pile:
            try:
                solutions.append(
                    find_solution(original_problem, pile, GUI_callback, try_next_solution(pile))
                )
            except NoSolutionError:
                pass
    print('#'*60, '\n')
    print('{} solution{} found:\n\n{}'.format(
        len(solutions),
        (' was' if len(solutions) == 1 else 's were'),
        '\n and \n'.join(str(s) for s in solutions))
    )
    print('\nSolving took {:.3f}s\n'.format(time.time()-start))
    print('#'*60)
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
    print('number of deadends:', nb_deadends)
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
    last_line = solution.shape[0] - 1
    last_col  = solution.shape[1] - 1

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

    if line == last_line:
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

    if col == last_col:
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

def draw_square(canvas, direction, l, c, square_size):
    center = (square_size * (c + 0.5), square_size * (l + 0.5))
    width = square_size // 10
    if direction == 'up':
        delta = (0, -square_size//2)
    elif direction == 'down':
        delta = (0, square_size//2)
    elif direction == 'right':
        delta = (square_size//2, 0)
    elif direction == 'left':
        delta = (-square_size//2, 0)
    canvas.create_line(center[0], center[1], center[0] + delta[0], center[1] + delta[1], fill='white', width=width)
    canvas.create_rectangle(center[0] - width//2, center[1] - width//2, center[0] + width//2, center[1] + width//2, fill='grey', outline='grey')

def draw(canvas, solution, solved=False, slow=False):
    global square_size
    canvas.delete('all')
    line, col = solution.shape
    for l in range(line):
        for c in range(col):
            shape = solution[l, c]
            for direction, shapes in LINES.items():
                if shape in shapes:
                    draw_square(canvas, direction, l, c, square_size)
    for l in range(1, line):
        canvas.create_line(0, square_size * l, square_size * col, square_size * l, fill='grey')
    for c in range(1, col):
        canvas.create_line(square_size * c, 0, square_size * c, square_size * line, fill='grey')

    if solved:
        canvas.configure(background='green')
    else:
        canvas.configure(background='red')

    if slow:
        import time
        time.sleep(0.1)
    canvas.update()


def GUI_solve(canvas, solution, slow):
    try:
        solutions = solve(
            solution,
            find_all=True,
            GUI_callback=lambda solution, valid=False: draw(canvas, solution, slow=slow, solved=valid)
        )
        solution = solutions.pop()
        draw(canvas, solution, solved=True)
    except NoSolutionError:
        print('This problem has no solution')

if __name__ == '__main__':
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
    problem3 = np.array([[3, 5, 5, 3, 3, 3, 1],
                         [3, 5, 5, 3, 3, 7, 1],
                         [1, 1, 3, 7, 3, 7, 3],
                         [1, 1, 3, 3, 3, 7, 3],
                         [1, 1, 3, 7, 3, 3, 1],
                         [3, 3, 3, 3, 1, 3, 1],
                         [0, 1, 3, 3, 1, 0, 1],
                         [1, 5, 5, 5, 3, 7, 3],
                         [3, 3, 3, 3, 0, 1, 0]],
                        dtype=np.int32).transpose()
    problem = problem3

    GUI = True
    SLOW_STEP = False
    INPUT_PROBLEM = True
    if INPUT_PROBLEM:
        print('Please type the problem')
        partial_problem = []
        partial_problem.append(input('> '))
        for i in range(len(partial_problem[0].split()) - 1):
            partial_problem.append(input('> '))
        clean_problem = []
        for line in partial_problem:
            for c in [('A', '10'), ('B', '11'), ('C', '12'), ('D', '13'), ('E', '14'), ('F', '15')]:
                line = line.replace(*c)
            clean_problem.append([int(shape) for shape in line.split()])
        problem = np.array(clean_problem, dtype=np.int32)
    if not GUI:
        try:
            solution = solve(problem, find_all=True)
        except NoSolutionError:
            print('#'*60, '\n')
            print('This problem has no solution\n')
            print('#'*60)
    else:
        global square_size
        square_size = 30
        line, col = problem.shape

        import tkinter
        root = tkinter.Tk()
        root.geometry('{}x{}'.format(square_size*col, 2*square_size*line + 50))

        canvas1 = tkinter.Canvas(root, width=square_size*col, height=square_size*line)
        draw(canvas1, problem)
        canvas1.configure(background='black')
        canvas1.pack()

        canvas2 = tkinter.Canvas(root, width=square_size*col, height=square_size*line)
        canvas2.configure(background='red')
        canvas2.pack()

        button = tkinter.Button(root, text='Solve', command=lambda: GUI_solve(canvas2, problem, SLOW_STEP)).pack(expand=1)
        root.mainloop()


