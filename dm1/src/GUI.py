from solver import LINES, solve

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


def draw(canvas, solution, solved=False, SHOW_STEPS=False):
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

    canvas.update()

    if SHOW_STEPS:
        import time
        time.sleep(0.1)
        if solved:
            time.sleep(0.3)


def GUI_solve(canvas, problem, FORWARD_CHECK, ARC_CONSISTENCY, SHOW_STEPS, FAST):
    from misc import console_print_solutions
    from time import time, sleep
    start = time()
    if FAST:
        solutions = solve(
            problem,
            FORWARD_CHECK=FORWARD_CHECK,
            ARC_CONSISTENCY=ARC_CONSISTENCY
        )
    else:
        solutions = solve(
            problem,
            FORWARD_CHECK=FORWARD_CHECK,
            ARC_CONSISTENCY=ARC_CONSISTENCY,
            GUI_callback=lambda solution, valid=False: draw(canvas, solution, SHOW_STEPS=SHOW_STEPS, solved=valid)
        )

    console_print_solutions(solutions, start)
    if solutions:
        global button
        button.pack_forget()
        while True:
            for solution in solutions:
                draw(canvas, solution, solved=True)
                sleep(0.8)


def start_GUI(problem, **params):
    global square_size, button
    square_size = 40

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

    def start_solving(event=None):
        GUI_solve(
            canvas2,
            problem,
            **params
        )
    root.bind('<Return>', start_solving)
    button = tkinter.Button(root, text='Solve', command=start_solving)
    button.pack(expand=1)

    root.mainloop()
