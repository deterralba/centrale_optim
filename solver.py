import numpy as np

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
TWO   = (3, 5, 6, 9, 10, 12)  # AC
THREE = (7, 11, 13, 14)       # BDE
FOUR  = (15, )
SHAPES_BY_SIZE = [ONE, TWO, THREE, FOUR]

class NoSolutionError(Exception):
    pass

def solve(original_problem, GUI_callback=lambda problem: None):
    nb_deadends = 0
    problem = np.zeros(original_problem.shape, dtype=np.int32) + DEFAULT_VALUE
    pile = []
    while not is_finished(problem):
        square = get_next_square(problem)
        choices = get_possible_choices(original_problem, problem, square)
        if choices:
            choice = choices.pop()
            problem[square] = choice
            GUI_callback(problem)
            import time
            #time.sleep(0.1)
            if choices:
                pile = add_choices_to_pile(problem, pile, square, choices)
        else:
            nb_deadends += 1
            problem = try_next_solution(pile)
            print('extract old problem from pile: ', problem)
            print('size of pile is', len(pile))
    print('number of deadends:', nb_deadends)
    return problem

def try_next_solution(pile):
    if pile:
        problem, square, choice = pile.pop()
        problem[square] = choice
        return problem
    else:
        raise NoSolutionError('no more entries in pile')

def add_choices_to_pile(problem, pile, square, choices):
    for choice in choices:
        pile.append((np.copy(problem), square, choice))
    return pile

def get_possible_choices(original_problem, problem, square):
    if original_problem[square] in [0, 15]:
        return list(original_problem[square])
    else:
        choices = []
        constrains = get_constrains(problem, square)
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

def get_constrains(problem, square):
    line, col = square
    last_line = problem.shape[0] - 1
    last_col  = problem.shape[1] - 1

    if line == 0:
        line_up = False
    else:
        up_square = problem[line - 1, col]
        if up_square == DEFAULT_VALUE:
            line_up = None
        elif up_square in LINE_DOWN:
            line_up = True
        else:
            line_up = False

    if line == last_line:
        line_down = False
    else:
        down_square = problem[line + 1, col]
        if down_square == DEFAULT_VALUE:
            line_down = None
        elif down_square in LINE_UP:
            line_down = True
        else:
            line_down = False

    if col == 0:
        line_left = False
    else:
        left_square = problem[line, col - 1]
        if left_square == DEFAULT_VALUE:
            line_left = None
        elif left_square in LINE_RIGHT:
            line_left = True
        else:
            line_left = False

    if col == last_col:
        line_right = False
    else:
        right_square = problem[line, col + 1]
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
    print('Constrains for {} {}: {}\nin {}'.format(line, col, lines, problem))
    return lines

def get_next_square(problem):
    for i in range(problem.shape[0]):
        for j in range(problem.shape[1]):
            if problem[i, j] == DEFAULT_VALUE:
                return (i, j)
    else:
        raise ValueError('no next square: {}'.format(problem))

def is_finished(problem):
    try:
        get_next_square(problem)
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

def draw(canvas, problem, solved=False):
    print('drawing', canvas, problem)
    global square_size, root
    canvas.delete('all')
    line, col = problem.shape
    for l in range(line):
        for c in range(col):
            shape = problem[l, c]
            for direction, shapes in LINES.items():
                if shape in shapes:
                    draw_square(canvas, direction, l, c, square_size)
    for l in range(1, line):
        canvas.create_line(0, square_size * l, square_size * col, square_size * l, fill='grey')
    for c in range(1, col):
        canvas.create_line(square_size * c, 0, square_size * c, square_size * line, fill='grey')
    if solved:
        canvas.configure(background='green')
    root.update()


def GUI_solve(canvas, problem):
    global canvas2
    try:
        solution = solve(problem, GUI_callback=lambda problem: draw(canvas, problem))
        draw(canvas, solution, solved=True)
    except NoSolutionError:
        print('This problem has no solution')

if __name__ == '__main__':
    problem = np.array([[1, 7, 3], [1, 3, 3], [3, 5, 1]], dtype=np.int32)
    print(problem)

    GUI = True
    if GUI:
        global square_size
        square_size = 60
        line, col = problem.shape

        import tkinter
        global button, canvas1, canvas2
        root = tkinter.Tk()
        root.geometry('{}x{}'.format(square_size*col, 2*square_size*line + 50))

        canvas1 = tkinter.Canvas(root, width=square_size*col, height=square_size*line)
        canvas1.configure(background='black')
        canvas1.pack()
        canvas2 = tkinter.Canvas(root, width=square_size*col, height=square_size*line)
        canvas2.configure(background='red')
        canvas2.pack()

        draw(canvas1, problem)
        button = tkinter.Button(root, text='Solve', command=lambda: GUI_solve(canvas2, problem)).pack(expand=1)
        root.mainloop()
    '''
    try:
        root = tkinter.Tk()
        solution = solve(problem)
        print(solution)
        draw(root, solution)
    except NoSolutionError:
        print('This problem has no solution')
    '''

