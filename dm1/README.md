## Installation

This solver requires Python 3 and `numpy`.

To use the GUI you will need tkinter, the default python GUI library. On debian/Ubuntu: `sudo apt-get install python3-tk`).

Note: You can use the program without GUI with the flag `--nogui`.

## Use

Examples

```
# print the help
$ .src/solver.py -h

# read the standard input
$ .src/solver.py -s

# solve an example (number between 0 and 4) and show all the steps
$ .src/solver.py -e 3 -p

# read the standard input and solve hide the steps (faster)
$ .src/solver.py -s -f

# disable the GUI
$ .src/solver.py -e 2 -n
```

## Misc

The shapes are :

![shapes](tuiles.svg)



